from configparser import ConfigParser

def load_config(filename='src/services/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    print(parser.sections())

    # pega a secao do arquivo database.ini
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for p in params:
            config[p[0]] = p[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return config