# Projeto de Web Scraping Con treinamentos

## Descrição
Este projeto consiste em criar um script de web scraping para coletar informações de um site específico.

## Objetivo
O objetivo deste projeto é demonstrar como realizar web scraping de forma eficiente e organizada, coletando dados relevantes do site alvo.

## Tecnologias Utilizadas
- Python
- Bibliotecas: Scrapy

## Instalação
1. Clone este repositório: `git clone https://github.com/letdevx/Scraping_Con_treinamentos.git`
2. Navegue para o diretório do projeto: `cd Scraping_Con_treinamentos`

## Uso
1. Execute o script de web scraping: `python main.py`
2. Os dados coletados serão armazenados no arquivo `results/contreinamentos_{time}.csv`.

## Estrutura do Projeto
Scraping_Con_treinamentos/</br>
│ Con_treinamentos</br>
│ | spiders</br>
| | | \_\_init\_\_.py</br>
| | │ conTreinamentos.py</br>
| | │ conTreinamentosUrls.py</br>
│ | results</br>
| | | contreinamentos_2023-08-28T15-10-01.csv</br>
| | | contreinamentosurls_2023-08-28T15-10-01.csv</br>
| | \_\_init\_\_.py</br>
| | items.py</br>
| | middlewares.py</br>
| | pipelines.py</br>
| | settings.py</br>
| venv/</br>
| .gitignore</br>
| main.py</br>
| README.md</br>
| scrapy.cfg


## Exemplo de Resultado
Aqui está um exemplo dos dados coletados e armazenados no arquivo `contreinamentos2023-08-16T16-54-10.csv` (o nome do arquivo muda conforme a data e horario em que ele foi gerado):

| Empresa      | Curso                                              | URL                                                             | Professor | Data                       | Local   | Carga Horária | Valor       |
|--------------|----------------------------------------------------|-----------------------------------------------------------------|-----------|----------------------------|---------|---------------|-------------|
| Con Treinamentos    | Treinamento de Cadastradores Parciais do SIAPE.   | https://onecursos.com.br/course/curso-online-treinamento-de-cadastradores-parciais-do-siape |  João da Silva         | 21/08/2023 a 25/08/2023    | online  | 20 horas      | R$ 2.290,00 |




