CREATE OR REPLACE FUNCTION calcular_sintonia_musical(user_id_input INT)
RETURNS TABLE(usuario_id INT, sintonia FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT
        outro.id,
        100.0 * SUM(CASE WHEN a1.feedback = a2.feedback THEN 1 ELSE 0 END)::float / COUNT(a1.id_musica) AS sintonia
    FROM
        usuario_avalia_musica a1
    JOIN
        usuario_avalia_musica a2 ON a1.id_musica = a2.id_musica
    JOIN
        usuario outro ON a2.id_usuario = outro.id
    WHERE
        a1.id_usuario = user_id_input
        AND a2.id_usuario != user_id_input
    GROUP BY
        outro.id;
END;
$$ LANGUAGE plpgsql;