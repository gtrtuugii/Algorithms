DELIMITER ++
CREATE FUNCTION isNutFree(coneNumber INT)
RETURNS BOOLEAN DETERMINISTIC
BEGIN
DECLARE tf BOOLEAN;

read_loop: LOOP
IF EXISTS(SELECT C.id
FROM  ScoopsInCone SC, Cone C, Scoop S
WHERE C.id = SC.coneId AND S.id = SC.scoopId 
AND coneNumber = C.id
AND C.conetype = 'Waffle'
AND S.name = 'Coconut' AND S.name = 'Macadamia')
THEN RETURN 0;
END IF;
IF EXISTS(SELECT C.id
FROM  ScoopsInCone SC, Cone C, Scoop S
WHERE C.id = SC.coneId AND S.id = SC.scoopId 
AND coneNumber = C.id
AND C.conetype = 'Waffle')
THEN RETURN 0;
END IF;
IF EXISTS(SELECT C.id
FROM  ScoopsInCone SC, Cone C, Scoop S
WHERE C.id = SC.coneId AND S.id = SC.scoopId
AND coneNumber = C.id
AND S.name = 'Coconut')
THEN RETURN 0;
END IF;
IF EXISTS(SELECT C.id
FROM  ScoopsInCone SC, Cone C, Scoop S
WHERE C.id = SC.coneId AND S.id = SC.scoopId
AND coneNumber = C.id
AND S.name = 'Macadamia')
THEN RETURN 0;
ELSE RETURN 1;
END IF;
END LOOP;

RETURN tf;

END++
DELIMITER ;