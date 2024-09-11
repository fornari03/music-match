-- Criacao do Banco

CREATE DATABASE "Spotinder"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


-- Criacao do usuario

    CREATE ROLE teste WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    NOBYPASSRLS
    CONNECTION LIMIT -1
    PASSWORD '12345';

GRANT pg_read_all_data, pg_write_all_data TO teste;

-- Criacao das tabelas

CREATE TABLE IF NOT EXISTS Usuario (
    id serial PRIMARY KEY,
    nome text,
    email text UNIQUE,
    senha text,
    data_nascimento date,
    foto_perfil bytea
);

CREATE TABLE IF NOT EXISTS Artista (
    id serial PRIMARY KEY,
    nome text UNIQUE,
    foto bytea
);

-- outra query

CREATE TABLE IF NOT EXISTS conecta_com (
    id_usuario_1 integer REFERENCES Usuario(id),
    id_usuario_2 integer REFERENCES Usuario(id),
    PRIMARY KEY (id_usuario_1, id_usuario_2)
);

CREATE TABLE IF NOT EXISTS redes_sociais (
    id_usuario integer REFERENCES Usuario(id),
    rede_social text,
    usuario_rede_social text,
    PRIMARY KEY(id_usuario, rede_social)
);

CREATE TABLE IF NOT EXISTS Musica
(
    id serial PRIMARY KEY,
    nome text,
    capa bytea,
    link_spotify text
);

CREATE TABLE IF NOT EXISTS Estilo_musical
(
    id serial PRIMARY KEY,
    nome text
);

CREATE TABLE IF NOT EXISTS Evento
(
    id serial PRIMARY KEY,
    nome text ,
    descricao text,
    localizacao text,
    data_realizacao timestamp,
    foto bytea
);

-- outra query

CREATE TABLE IF NOT EXISTS pertence_ao 
(
    id_musica integer REFERENCES Musica(id),
    id_estilo_musical integer REFERENCES Estilo_musical(id),
    PRIMARY KEY(id_musica, id_estilo_musical)
);

CREATE TABLE IF NOT EXISTS evento_tem_estilo_musical 
(
    id_evento integer REFERENCES Evento(id),
    id_estilo_musical integer REFERENCES Estilo_musical(id),
    PRIMARY KEY(id_evento, id_estilo_musical)
);

CREATE TABLE IF NOT EXISTS artista_tem_musica
(
    id_artista integer REFERENCES Artista(id),
    id_musica integer REFERENCES Musica(id),
    PRIMARY KEY(id_artista, id_musica)
);

CREATE TABLE IF NOT EXISTS participa
(
    id_artista integer REFERENCES Artista(id),
    id_evento integer REFERENCES Evento(id), 
    PRIMARY KEY(id_artista, id_evento)
);

CREATE TABLE IF NOT EXISTS tem_interesse
(
    id_usuario integer REFERENCES Usuario(id),
    id_evento integer REFERENCES Evento(id), 
    PRIMARY KEY(id_usuario, id_evento)
);

CREATE TABLE IF NOT EXISTS participou_de
(
    id_usuario integer REFERENCES Usuario(id),
    id_evento integer REFERENCES Evento(id), 
    PRIMARY KEY(id_usuario, id_evento)
);

CREATE TABLE IF NOT EXISTS usuario_avalia_musica
(
    id_usuario integer REFERENCES Usuario(id),
    id_musica integer REFERENCES Musica(id), 
    feedback boolean,
    PRIMARY KEY(id_usuario, id_musica)
);