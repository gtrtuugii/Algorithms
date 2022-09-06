SELECT flavour.name
FROM (SELECT MAX(costInCents) as price, Scoop.name as name
FROM Scoop
GROUP BY name
ORDER BY price DESC) AS flavour;