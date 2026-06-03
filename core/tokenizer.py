def tokenize_receta(texto: str):

    texto = texto.lower()

    texto = (
        texto.replace("á", "a")
             .replace("é", "e")
             .replace("í", "i")
             .replace("ó", "o")
             .replace("ú", "u")
    )

    lineas = texto.split('\n')

    tokens = []

    for linea in lineas:

        linea = linea.strip()

        if linea:

            tokens.extend(token.replace("<eos>", "<EOS>") for token in linea.split())
            tokens.append('<EOS>')

    return tokens


def normalize_token(token: str):
    return (
        token.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )
