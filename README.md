# MusicMatch
Repositório para o projeto da disciplina de Bancos de Dados.


Link para o repositório no GitHub: https://github.com/fornari03/music-match

## Introdução
O Music Match é um aplicativo com uma temática musical onde é possível estabelecer conexões com outros usuários a fim de conhecer novas pessoas, classificar eventos onde o usuário esteve presente, "divulgar" os eventos em que há interesse e os que não há interesse. Além disso, também é possível avaliar músicas, o que irá permitir visualizar outros usuários e suas respectivas afinidades musicais entre si, a fim de estabelecer uma conexão musical, o `Music Match`! Para a implementação do nosso aplicativo, utilizamos a linguagem de programação Python, em que o front-end foi implementado com o uso da biblioteca Kivy MD e a conexão com o banco de dados foi feita com a biblioteca psycopg2. O SGBD utilizado foi o PostgreSQL.

## Modelo Entidade Relacionamento
![Modelo Entidade Relacionamento](https://github.com/user-attachments/assets/d1ee99fe-5299-424a-b4a7-93bc2889dbbc)



## Modelo Relacional
![Diagrama Modelo Relacional](https://github.com/user-attachments/assets/05263f7b-e672-4a76-a6f2-7ea6cbb35cb6)

## Consultas em álgebra relacional
### Consulta 1: Encontrar todas as músicas de um estilo musical específico, junto com o artista que as compôs.

π_Musica.nome, Artista.nome
(σ_Estilo_musical.nome='Rock'
 (Musica ⨝ pertence_ao ⨝ Estilo_musical ⨝ artista_tem_musica ⨝ Artista))

Tabelas envolvidas:

Musica: contém as informações das músicas.

Artista: contém as informações dos artistas.

artista_tem_musica: relaciona músicas com seus respectivos artistas.

pertence_ao: relaciona músicas com seus estilos musicais.

Estilo_musical: contém os nomes dos estilos musicais.

Descrição: A consulta começa selecionando os estilos musicais cujo nome seja "Rock". Em seguida, realiza junções entre as tabelas Musica, artista_tem_musica, Artista, pertence_ao e Estilo_musical. O objetivo é encontrar o nome das músicas e seus respectivos artistas associados ao estilo "Rock".


### Consulta 2: Listar todos os eventos que envolvem um estilo musical específico e os artistas que participam deles.

π_Evento.nome, Artista.nome
(σ_Estilo_musical.nome='Jazz'
 (Estilo_musical ⨝ evento_tem_estilo_musical ⨝ Evento ⨝ participa ⨝ Artista))


Tabelas envolvidas:

Evento: contém as informações dos eventos.

Artista: contém as informações dos artistas.

participa: relaciona artistas com eventos.

evento_tem_estilo_musical: relaciona eventos com estilos musicais.

Estilo_musical: contém os nomes dos estilos musicais.

Descrição: A consulta filtra eventos cujo estilo musical seja "Jazz". As tabelas Evento, participa, Artista, evento_tem_estilo_musical e Estilo_musical são unidas para encontrar os eventos e os artistas que participaram deles, relacionados ao estilo musical "Jazz".


### Consulta 3: Encontrar os usuários que avaliaram uma música com um estilo musical específico.

π_Usuario.nome, Musica.nome
(σ_Estilo_musical.nome='Pop'
 (Usuario ⨝ usuario_avalia_musica ⨝ Musica ⨝ pertence_ao ⨝ Estilo_musical))

Tabelas envolvidas:

Usuario: contém as informações dos usuários.

usuario_avalia_musica: relaciona usuários com músicas avaliadas.

Musica: contém as informações das músicas.

pertence_ao: relaciona músicas com seus estilos musicais.

Estilo_musical: contém os nomes dos estilos musicais.

Descrição: A consulta procura por músicas do estilo "Pop" que foram avaliadas por usuários. As tabelas Usuario, usuario_avalia_musica, Musica, pertence_ao e Estilo_musical são unidas para identificar os usuários e as músicas que eles avaliaram, relacionadas ao estilo "Pop".


### Consulta 4: Encontrar todos os usuários que têm interesse em um evento específico, junto com o nome do evento.

π_Usuario.nome, Evento.nome
(σ_Evento.id=1
 (Usuario ⨝ tem_interesse ⨝ Evento))

Tabelas envolvidas: 

Usuario: contém informações dos usuários.

tem_interesse: relaciona usuários aos eventos nos quais eles têm interesse.

Evento: contém informações dos eventos.

A seleção (σ) filtra os registros da tabela Evento para o evento específico com id = 1.

As junções (⨝) conectam as tabelas Usuario, tem_interesse e Evento para formar um conjunto de dados que relaciona usuários aos eventos de interesse.

A projeção (π) retorna os nomes dos usuários e o nome do evento.


### Consulta 5: Listar todos os eventos em que um artista específico participa.

π_Evento.nome
(σ_Artista.id=2
 (Evento ⨝ participa ⨝ Artista))


Tabelas envolvidas:

Evento: contém informações dos eventos.

Artista: contém informações dos artistas.

participa: relaciona artistas aos eventos nos quais eles participam.

A seleção (σ) filtra os registros da tabela Artista para o artista específico com id = 2.

As junções (⨝) conectam as tabelas Evento, participa e Artista para formar um conjunto de dados que relaciona eventos ao artista.

A projeção (π) retorna os nomes dos eventos em que o artista participa. 

## Avaliação das formas normais das tabelas

### USUÁRIO

#### PRIMEIRA FORMA NORMAL ########

A tabela "Usuario" é minimamente normalizada, ou seja, está na primeira forma normal, visto que todos os seus atributos id, nome, email, senha e data de nascimento contém dados atômicos, contendo apenas um valor por registro.

#### SEGUNDA FORMA NORMAL #########

A tabela "Usuario" está na segunda forma normal, pois, além de estar na primeira forma normal, os atributos complementos da chave candidata id são totalmente funcionalmente dependente da mesma, ou seja, para todos os valores dos atributos nome, email, senha e data de nascimento, há apenas um valor de id e id não é funcionalmente dependente de nome, email, senha ou data de nascimento.

#### TERCEIRA FORMA NORMAL

A tabela "Usuario" está na terceira forma normal, pois, além de estar na segunda forma normal, não há dependentes transitivos da chave primária id dentre os atributos nome, email, senha e data de nascimento, ou seja, os campos não seriam dependentes diretamente da chave primária e nem dependentes de outro campo não-chave.


### EVENTO

#### PRIMEIRA FORMA NORMAL

A tabela "Evento" é minimamente normalizada, ou seja, está na primeira forma normal, visto que todos os seus atributos id, nome, data, localizacao e descricao contém dados atômicos, contendo apenas um valor por registro.

#### SEGUNDA FORMA NORMAL

A tabela "Evento" está na segunda forma normal, pois, além de estar na primeira forma normal, os atributos complementos da chave candidata id são totalmente funcionalmente dependente da mesma, ou seja, para todos os valores dos atributos nome, data, localizacao e descricao, há apenas um valor de id e id não é funcionalmente dependente de nome, data, localizacao e descricao.

#### TERCEIRA FORMA NORMAL

A tabela "Evento" está na terceira forma normal, pois, além de estar na segunda forma normal, não há dependentes transitivos da chave primária id dentre os atributos nome, data, localizacao e descricao, ou seja, os campos não seriam dependentes diretamente da chave primária e nem dependentes de outro campo não-chave.

### MÚSICA

#### PRIMEIRA FORMA NORMAL ########

A tabela "Musica" é minimamente normalizada, ou seja, está na primeira forma normal, visto que todos os seus atributos id, nome, capa e link_spotify contém dados atômicos, contendo apenas um valor por registro.

##### SEGUNDA FORMA NORMAL #########

A tabela "Musica" está na segunda forma normal, pois, além de estar na primeira forma normal, os atributos complementos da chave candidata id são totalmente funcionalmente dependente da mesma, ou seja, para todos os valores dos atributos nome, capa e link_spotify, há apenas um valor de id e id não é funcionalmente dependente de nome, capa e link_spotify.

##### TERCEIRA FORMA NORMAL

A tabela "Musica" está na terceira forma normal, pois, além de estar na segunda forma normal, não há dependentes transitivos da chave primária id dentre os atributos nome, capa e link_spotify, ou seja, os campos não seriam dependentes diretamente da chave primária e nem dependentes de outro campo não-chave. A capa não depende funcionalmente do link_spotify, pois ela é obtida da internet ao invés da api do spotify.

### ARTISTA

##### PRIMEIRA FORMA NORMAL

A tabela "Artista" é minimamente normalizada, ou seja, está na primeira forma normal, visto que todos os seus atributos id, nome e foto contém dados atômicos, contendo apenas um valor por registro.

#### SEGUNDA FORMA NORMAL

A tabela "Artista" não está na segunda forma normal, pois o atributo foto é sempre NULL, pois não foi possível utilizá-lo na aplicação.

#### TERCEIRA FORMA NORMAL

A tabela "Musica" está na terceira forma normal, pois não está na segunda forma normal.

### ESTILO MUSICAL

##### PRIMEIRA FORMA NORMAL

A tabela "Estilo Musical" é minimamente normalizada, ou seja, está na primeira forma normal, visto que todos os seus atributos id e nome contém dados atômicos, contendo apenas um valor por registro.

##### SEGUNDA FORMA NORMAL

A tabela "Musica" está na segunda forma normal, pois, além de estar na primeira forma normal, os atributos complementos da chave candidata id são totalmente funcionalmente dependente da mesma, ou seja, para todos os valores do atributo nome, há apenas um valor de id e id não é funcionalmente dependente de nome.

##### TERCEIRA FORMA NORMAL

A tabela "Musica" está na terceira forma normal, pois, além de estar na segunda forma normal, não há dependentes transitivos da chave primária id para o atributo nome, ou seja, os campos não seriam dependentes diretamente da chave primária e nem dependentes de outro campo não-chave.

## Camada de persistência

![Diagrama da camada de persistência](https://github.com/user-attachments/assets/28029151-cbee-48b3-bce7-0d530d8c24a0)
