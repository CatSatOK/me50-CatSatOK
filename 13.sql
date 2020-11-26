--names of all people who starred in a movie in which Kevin Bacon also starred.
--There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
--Kevin Bacon himself should not be included in the resulting list

SELECT DISTINCT name
FROM stars JOIN people ON stars.person_id = people.id
WHERE movie_id IN
(SELECT movie.id
FROM people JOIN stars ON stars.person_id = people.id
WHERE name = "Kevin Bacon" and birth = 1958)
AND name != "Kevin Bacon";
