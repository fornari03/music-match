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
