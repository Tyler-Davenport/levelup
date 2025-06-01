-- SELECT * FROM levelupapi_gamer;
-- SELECT * FROM levelupapi_gametype;
-- SELECT * FROM levelupapi_game;
-- SELECT * FROM levelupapi_event;
DELETE FROM levelupapi_gamer WHERE uid = 'oO9Q3zBVXpQ2ks6PFZMkfEkqkpB3' AND id != (SELECT MIN(id) FROM levelupapi_gamer WHERE uid = 'oO9Q3zBVXpQ2ks6PFZMkfEkqkpB3');
