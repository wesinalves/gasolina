import requests


def download_file(url):
    """Downloads a file from a url and returns the filename."""
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)
    return file_name


def main():
    """Main function."""
    url_base = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca"
    for i in range(2004, 2022):
        url1 = f"{url_base}-{i}-01.csv"
        url2 = f"{url_base}-{i}-02.csv"
        file1 = download_file(url1)
        file2 = download_file(url2)
        print("Downloaded file: " + file1)
        print("Downloaded file: " + file2)


main()
