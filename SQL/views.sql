CREATE OR REPLACE VIEW artistas_mais_curtidos AS
	SELECT ar.nome, ar.id, av.id_usuario FROM usuario_avalia_musica av
		JOIN artista_tem_musica atm ON av.id_musica = atm.id_musica
		JOIN artista ar ON atm.id_artista = ar.id WHERE av.feedback=TRUE
		GROUP BY ar.id, ar.nome, av.id_usuario ORDER BY COUNT(*) DESC;

CREATE OR REPLACE VIEW estilos_mais_curtidos AS
	SELECT em.nome, em.id, av.id_usuario FROM usuario_avalia_musica av
		JOIN pertence_ao pa ON av.id_musica = pa.id_musica
		JOIN estilo_musical em ON pa.id_estilo_musical = em.id
		WHERE av.feedback = TRUE
		GROUP BY em.id, em.nome, av.id_usuario ORDER BY COUNT(*) DESC