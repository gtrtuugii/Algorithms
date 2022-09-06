def write_reversed_file(input_filename, output_filename):
    with open(output_filename, 'w') as f:
	with open(input_filename, 'r') as r:
	    for line in reversed(list(r.read())):
		f.write(line)
