
// used to access e.g. seteuid
#define _POSIX_C_SOURCE 200809L

#include "curdle.h"

/** \file adjust_score.c
 * \brief Functions for safely amending a player's score in the
 * `/var/lib/curdle/scores` file.
 *
 * Contains the \ref adjust_score_file function, plus supporting data
 * structures and functions used by that function.
 *
 * ### Known bugs
 *
 * \bug The \ref adjust_score_file function does not yet work.
 */

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <string.h>

// used for fstat, lseek
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

// naming:
// Where we have a preprocessor symbol and a `const` value
// for the same entity, we suffix the preprocessor symbol
// with an underscore ("_").

/** Size of a field (name or score) in a line of the `scores`
  * file.
  */
const size_t FIELD_SIZE = FIELD_SIZE_;

/** Size of a line in the `scores` file.
  */
const size_t REC_SIZE   = REC_SIZE_;

// #define-ing this allows us to easily switch it out
// at compile time with a test file-path
#define SCORES_FILE_PATH_ "/var/lib/curdle/scores"

const char* SCORES_FILE_PATH = SCORES_FILE_PATH_;

const long MIN_STORABLE_SCORE = -999999999l;
const long MAX_STORABLE_SCORE = 9999999999l;

// assert that we can store a positive ssize_t in a size_t;
// assuming that's the case, we can safely assign any positive
// size_t to a size_t without wraparound.
static_assert( SSIZE_MAX <= SIZE_MAX, "positive ssize_t storable in size_t" );

// Assert that we an off_t is just a long;
// and then that we can safely store a positive off_t/long in a size_t
// without wraparound.
// Should be true on the platform we're compiling for (Linux on x86-64
// using glibc), but ideally should fail noisily on an attempt to
// port this to an incompatible platform.

// same_type(T1, T2):
// the macro returns 1 if T1 and T2 are the same type,
// 0 if they differ.
//
// Implementation details: uses _Generic and compound literals
// to compare types: see
// <https://stackoverflow.com/questions/58018332/can-c11s-generic-keyword-be-used-within-gcc-static-assert>
#define same_type(T1, T2) _Generic((  (T1){0}  ), \
  T2: 1, \
  default: 0 \
)

static_assert( same_type(off_t, long), "off_t is a long");
static_assert( LONG_MAX <= SIZE_MAX, "positive long storable in size_t");


/** version of score_record that stores a `long`
 * and can thus safely represent all storable values
 */
struct score_record_l {
  /** The name of the player a score is being recorded for. */
  char name[FIELD_SIZE_];
  /** The current score for the player. */
  long  score;
};

// safe addition of two signed `long`s.
// (Doesn't check whether the result can be safely _stored_;
// that's done by store_record
long safe_add(long a, long b) {
  if (a > 0 && b > LONG_MAX - a)
    die(__FILE__, __LINE__, "safe_add: a + b would exceed max limit of long");
  if (a < 0 && b < LONG_MIN - a)
    die(__FILE__, __LINE__, "safe_add: a + b would go below lower limit of long");
  return a + b;
}

/** Initialize a \ref score_record_l struct.
  *
  * \param rec pointer to a \ref score_record_l struct to initialize.
  * \param name player name to be inserted into `rec`.
  * \param score player score to be inserted into `rec`.
  */
void score_record_init(struct score_record_l *rec, const char *name, int score) {
  // this function is needed to initialize a score_record_l,
  // because you can't *assign* to the name member -- it's an array.
  // so we must copy the name in.
  memset(rec->name, 0, FIELD_SIZE);
  strncpy(rec->name, name, FIELD_SIZE);
  rec->name[FIELD_SIZE-1] = '\0';
  rec->score = score;
}

#include <fcntl.h>


/** Adjust the score for player `player_name`, incrementing it by
  * `score_to_add`. The player's current score (if any) and new score
  * are stored in the scores file at `/var/lib/curdle/scores`.
  * The scores file is owned by user ID `uid`, and the process should
  * use that effective user ID when reading and writing the file.
  * If the score was changed successfully, the function returns 1; if
  * not, it returns 0, and sets `*message` to the address of
  * a string containing an error message. It is the caller's responsibility
  * to free `*message` after use.
  *
  * \param uid user ID of the owner of the scores file.
  * \param player_name name of the player whose score should be incremented.
  * \param score_to_add amount by which to increment the score.
  * \param message address of a pointer in which an error message can be stored.
  * \return 1 if the score was successfully changed, 0 if not.
  */
int adjust_score(uid_t uid, const char * player_name, int score_to_add, char **message);


/** Return the size of the open file with file descriptor `fd`.
  * If the size cannot be determined, the function may abort program
  * execution (optionally after printing an error message).
  *
  * `filename` is used for diagnostic purposes only, and may be `NULL`.
  * If non-NULL, it represent the name of the file path from which
  * `fd` was obtained.
  *
  * \param filename name of the file path from which `fd` was obtained.
  * \param fd file descriptor for an open file.
  * \return the size of the file described by `fd`.
  */
size_t file_size(const char * filename, int fd);

// Below are 2 alternative implementations of file_size, based
// on fast and lseek, respectively. Either will work.



// filename is purely for diagnostic purposes
// works out file size based on result of fstat
off_t fstat_size(const char * filename, int fd) {
  // unused
  (void)(filename);

  struct stat file_stats;
  // sanity-check file size
  int res = fstat(fd, &file_stats);
  if (res == -1) {
    // todo: string cat
    die_perror(__FILE__, __LINE__, "fstat_size: couldn't get fstat on input file");
    exit(1);
  } else if (res < 0) {
    die(__FILE__, __LINE__, "fstat_size: impossible return value");
  }
  off_t size = file_stats.st_size;
  if (size < 0) {
    die(__FILE__, __LINE__, "fstat_size: found impossible negative size");
  }
  return size;
}

size_t file_size(const char * filename, int fd) {
  return fstat_size(filename, fd);
}

// filename is purely for diagnostic purposes
// works out file size based on result of lseek
// leaves the file offset repositioned at the end
off_t lseek_size(const char * filename, int fd) {
  // unused
  (void)(filename);

  // WARNING: make sure we don't truncate end_pos
  off_t end_pos = lseek(fd, 0, SEEK_END);
  if (end_pos == -1) {
    die_perror(__FILE__, __LINE__, "lseek_size: couldn't seek to end of file");
  }
  return end_pos;
}

/** Parse a \ref score_record_l struct from an
  * array of size \ref REC_SIZE.
  *
  * If a name and score cannot be found in `rec_buf`,
  * the function may abort program
  * execution (optionally after printing an error message).
  *
  * \param rec_buf an array of size \ref REC_SIZE.
  * \return a parsed \ref score_record_l.
  */
struct score_record_l parse_record(char rec_buf[REC_SIZE]) {
  struct score_record_l rec = { "", 0 };
  // we're guaranteed first field is no more than 9 chars.
  // so there's no harm forcefully inserting a NUL
  // at the 10th character (offset 9).
  rec_buf[FIELD_SIZE-1] = '\0';
  size_t name_len = strlen(rec_buf);
  if (name_len >= FIELD_SIZE) {
    die(__FILE__, __LINE__, "parse_record: found name longer than 9 chars");
  }
  strncpy(rec.name, rec_buf, FIELD_SIZE);
  rec.name[FIELD_SIZE-1] = '\0';
  char * score_end = NULL;

  // the second field can be up to 10 characters, with no
  // terminating nul.
  // So copy it into something which _does_ have the
  // terminating nul.
  char num_buf[FIELD_SIZE+1];
  memcpy(num_buf, rec_buf + FIELD_SIZE, FIELD_SIZE);
  num_buf[FIELD_SIZE] = '\0';

  long lscore = strtol(num_buf, &score_end, 10);
  // cases:
  // nothing was read:
  if (score_end == rec_buf + FIELD_SIZE) {
    die(__FILE__, __LINE__, "parse_record: no chars converted for strtol()");
  }
  // whole string was valid
  if (score_end != NULL && score_end[0] == '\0') {
    // the value stored must necessarily be
    // between MIN_STORABLE_SCORE and MAX_STORABLE_SCORE;
    // but no harm checking.
    if (lscore < MIN_STORABLE_SCORE || lscore > MAX_STORABLE_SCORE) {
      die(__FILE__, __LINE__, "parse_record: impossible! found score outside storable score range");
    }
    rec.score = lscore;
    return rec;
  }
  die(__FILE__, __LINE__, "parse_record: string not entirely valid for strtol()");
}

/** Stores the player name and score in `rec` into a buffer of size
  * \ref REC_SIZE, representing a line from the scores file.
  *
  * The fields of rec should contain values that are valid for the
  * scores file; if not, the behaviour of the function is undefined.
  *
  * If the caller passes a buffer of size less than \ref REC_SIZE,
  * the behaviour of function is undefined.
  *
  * \param buf a `char` array of size \ref REC_SIZE.
  * \param rec pointer to a player's score record.
  */
void store_record(char buf[REC_SIZE], const struct score_record_l *rec) {
  // - Scores are passed around in `score_record_l` as a long,
  //   and are only stored if they physically fit into the field;
  //   if they do, they're valid.
  // - could use `snprintf_s()` (safer than snprintf) if available

  // clear buf, for safety. Makes conts of buf more reproducible.
  memset(buf, 0, REC_SIZE);
  // copy name
  memcpy(buf, rec->name, FIELD_SIZE);

  // copy score.
  // we do it in 2 steps:
  // 1. make a temp buf big enough to hold score+nul;
  // 2. copy that (except for final nul) back into buf
  char score_buf[FIELD_SIZE+1];
  memset(score_buf, 0, FIELD_SIZE+1);
  // we get the num chars required
  int num_chars_needed = snprintf(score_buf, FIELD_SIZE+1, "%ld", rec->score);
  if ((size_t) num_chars_needed > FIELD_SIZE) {
    die_perror(__FILE__, __LINE__, "store_record: score to big to store in FIELD_SIZE bytes");
  }
  // copy to buf
  memcpy(buf + FIELD_SIZE, score_buf, FIELD_SIZE);
  // set last char to newline
  buf[REC_SIZE-1] = '\n';
}

/** search within the open scores file with file descriptor
  * `fd` for a line containing the score for `player_name`.
  * If no such line exists, -1 is returned; otherwise, the
  * offset within the file is returned.
  *
  * `filename` is used only for diagnostic purposes.
  *
  * \param filename name of the file described by `fd`.
  * \param fd file descriptor for an open scores file.
  * \param player_name player name to seek for.
  * \return position in the file where a record can be found,
  *   or -1 if no no such record exists.
  */
off_t find_record(const char * filename, int fd, const char * player_name) {
  // get file size
  size_t size = file_size(filename, fd);

  // go to start
  off_t start_pos = lseek(fd, 0, SEEK_SET);
  if (start_pos == -1) {
    die_perror(__FILE__, __LINE__, "find_record: couldn't seek to start of file");
  }

  size_t num_records = size / REC_SIZE;

  for (size_t i = 0; i < num_records; i++) {
    // go to record
    off_t record_offset = REC_SIZE * i;
    off_t res = lseek(fd, record_offset, SEEK_SET);
    if (res == -1) {
      die_perror(__FILE__, __LINE__, "find_record: couldn't seek to record");
    }
    char rec_buf[REC_SIZE];
    ssize_t resx = read(fd, rec_buf, REC_SIZE);
    if (resx == -1) {
      die_perror(__FILE__, __LINE__, "find_record: couldn't read record");
    }
    size_t resx_ = resx;
    if (resx_ < REC_SIZE) {
      die_perror(__FILE__, __LINE__, "find_record: short read when trying to read record");
    }
    struct score_record_l rec = parse_record(rec_buf);
    // compare
    if (strlen(rec.name) == 0 && strlen(player_name) == 0)
      return record_offset;
    if (strncmp(rec.name, player_name, REC_SIZE) == 0)
      return record_offset;
  }
  return -1;
}

/** Adjust the score for player `player_name` in the open file
  * with file descriptor `fd`, incrementing it by
  * `score_to_add`. If no record for a player with that name
  * is found in the file, then one is created and appended to
  * the file.
  *
  * The `filename` parameter is purely for diagnostic purposes.
  *
  * If the file is not a valid "scores" file, or player name is
  * longer than the allowable length for a score record,
  * the function may abort program execution.
  *
  * \param filename name of the file from which `fd` was obtained.
  * \param fd file descriptor for an open scores file.
  * \param player_name name of the player whose score should be incremented.
  * \param score_to_add amount by which to increment the score.
  */
void adjust_score_file(const char * filename, int fd, const char * player_name, int score_to_add) {
  off_t record_locn = find_record(filename, fd, player_name);
  if (record_locn == -1) {
    // seek to end, make new record
    off_t res = lseek(fd, 0, SEEK_END);
    if (res == -1) {
      die_perror(__FILE__, __LINE__, "adjust_score_file: couldn't seek to end");
    }
    // construct new record
    struct score_record_l rec;
    score_record_init(&rec, player_name, score_to_add);
    // store to buf
    // room for one record
    char rec_buf[REC_SIZE];
    store_record(rec_buf, &rec);
    // write buf to file
    ssize_t write_res = write(fd, rec_buf, REC_SIZE);

    if (write_res == -1) {
      die_perror(__FILE__, __LINE__, "adjust_score_file: failed to write record");
    }
    size_t write_res_ = write_res;
    if (write_res_ < REC_SIZE) {
      die_perror(__FILE__, __LINE__, "adjust_score_file: short write of record");
    }
    return;
  }

  off_t res = lseek(fd, record_locn, SEEK_SET);
  if (res == -1) {
    die_perror(__FILE__, __LINE__, "adjust_score_file: couldn't seek to record");
  }

  // room for one record
  char rec_buf[REC_SIZE];
  ssize_t resx = read(fd, rec_buf, REC_SIZE);
  if (resx == -1) {
    die_perror(__FILE__, __LINE__, "adjust_score_file: couldn't read record");
  }
  size_t resx_ = resx;
  if (resx_ < REC_SIZE) {
    die_perror(__FILE__, __LINE__, "adjust_score_file: short read when trying to read record");
  }
  struct score_record_l rec = parse_record(rec_buf);
  rec.score = safe_add(rec.score, score_to_add);
  // store back to buf
  store_record(rec_buf, &rec);
  // and store buf back to file
  res = lseek(fd, record_locn, SEEK_SET);
  if (res == -1) {
    die_perror(__FILE__, __LINE__, "adjust_score_file: couldn't seek to record");
  }
  ssize_t write_res = write(fd, rec_buf, REC_SIZE);

  if (write_res == -1) {
    die_perror(__FILE__, __LINE__, "adjust_score_file: failed to write record");
  }
  size_t write_res_ = write_res;
  if (write_res_ < REC_SIZE) {
    die_perror(__FILE__, __LINE__, "adjust_score_file: short write of record");
  }

}

int adjust_score(uid_t uid, const char * player_name, int score_to_add, char **message) {
  // - We save the original euid & switch back to it after file-open.
  //  (There are alternative methods, but this is simple.)
  // - We don't open with O_CREAT; so if the file doesn't exist, the call to open
  //   should fail.

  // unused -- we don't use message to report errors, just die
  (void) message;
 
  uid_t orig_euid = geteuid();

  if (seteuid(uid) == -1) {
    die(__FILE__, __LINE__, "couldn't set effective uid to 'curdle' user");
  }

  int fd = open(SCORES_FILE_PATH, O_RDWR);

  if (seteuid(orig_euid) == -1) {
    die(__FILE__, __LINE__, "couldn't restore effective uid");
  }
  adjust_score_file(SCORES_FILE_PATH, fd, player_name, score_to_add);

  // if still here, we must have succeeded
  return 1;
}



