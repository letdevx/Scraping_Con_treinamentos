from datetime import datetime
import re
import scrapy


class ContreinamentosSpider(scrapy.Spider):
    """Spider responsável por coletar os cursos do site da empresa ConTreinamentos."""
    name = "conTreinamentos"
    start_urls = ["https://contreinamentos.com.br/cursos/"]
    time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    custom_settings = {
        'FEEDS': {
            f'results/contreinamentos_{time}.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        """Descobre os links dos cursos e dos eventos, 
        e delega a raspagem para metodos especificos."""
        links_cursos = response.xpath(
            '//*[@id="content"]//div[@class="elementor-container elementor-column-gap-default"]//div[@class="elementor-widget-wrap elementor-element-populated"]//div[@class="elementor-button-wrapper"]/a')
        links_eventos = response.xpath(
            '//*[@id="content"]//div[@class="elementor-flip-box"]//a')
        yield from response.follow_all(links_cursos, self.parse_curso)
        yield from response.follow_all(links_eventos, self.parse_evento)

    def parse_curso(self, response):
        """Executa a raspagem de dados de um curso."""
        section = response.xpath(
            '//div[contains(@id, "content")]/div/section[1]')
        con_treinamentos = "Con Treinamentos"
        tipo_evento = 'Curso'
        nome_curso = section.xpath('.//h2/text()').extract_first()
        if not nome_curso:
            nome_curso = section.xpath('.//img/@alt').extract()

        detalhes = section.xpath(
            './/p[contains(@class, "elementor-icon-box-description")]/text()').extract()
        nome_professor = detalhes[0].strip()
        data = detalhes[1].strip()
        local = '' if len(detalhes) < 3 else detalhes[2].strip()
        carga = response.xpath(
            '//*[@id="content"]/div/section[5]/div[3]/div[1]/div/div[3]/div/text()').extract_first()
        if not carga:
            carga = response.xpath(
                '//*[@id="content"]/div/section[4]/div[3]/div[1]/div/div[3]/div/text()').extract_first()
        lista_valor_curso = []
        modalidade = response.xpath(
            '//*[@id="content"]/div/section[5]/div[3]/div[3]/div/div[2]/div/h3/text()').extract_first()

        if modalidade == 'Híbrido':
            infos = data.split('-')
            data = infos[0]
            local = infos[1]
            valor_curso_presencial = response.xpath(
                '//*[@id="investimento"]/div/div/div/section/div/div[1]/div/div/div/div/div[2]/span[2]/text()').extract_first().strip()
            valor_curso_presencial += response.xpath(
                '//*[@id="investimento"]/div/div/div/section/div/div[1]/div/div/div/div/div[2]/div/span/text()').extract_first().strip()
            valor_curso_online = response.xpath(
                '//*[@id="investimento"]/div/div/div/section/div/div[2]/div/div/div/div/div[2]/span[2]/text()').extract_first().strip()
            valor_curso_online += response.xpath(
                '//*[@id="investimento"]/div/div/div/section/div/div[2]/div/div/div/div/div[2]/div/span/text()').extract_first().strip()
            lista_valor_curso.append(valor_curso_presencial)
            lista_valor_curso.append(valor_curso_online)
        else:
            valor_curso_presencial = response.xpath('//*[@id="investimento"]').xpath(
                './/div[contains(@class, "elementor-widget-container")]/text()')[4].extract()
            lista_valor_curso.append(valor_curso_presencial)

        for i, valor_curso in enumerate(lista_valor_curso):
            if i == 1:
                local = ''
            yield {
                'Empresa': con_treinamentos,
                'Curso': nome_curso,
                'Tipo': tipo_evento,
                'url': response.url,
                'Professor': nome_professor,
                'Data': data,
                'Local': local if local != '' else 'online',
                'carga-horaria': carga.strip() if carga else '',
                'Valor': valor_curso.strip(),
            }

    def parse_evento(self, response):
        """Executa a raspagem de dados de um evento."""
        section = response.xpath(
            '//div[contains(@id, "content")]/div/section[1]')
        con_treinamentos = 'Con Treinamentos'
        tipo_evento = 'Congresso'
        nome_curso = section.xpath('.//img/@alt').extract()
        data_congresso = section.xpath('.//h2/text()').extract_first()
        infos = data_congresso.split('-')
        data_congresso = infos[0]
        local_congresso = infos[1]
        if not re.search('[a-zA-Z]+\/\d{4}', data_congresso):
            aux = section.xpath('.//h3/text()').extract_first().split('-')
            data_congresso = aux[0]
            local_congresso = aux[1]
        professores = response.xpath(
            '//*[@id="especialistas"]/div/div/div/div/div/div/div/section/div/div/div/div/div/div/div[1]/div/div/div/text()').extract()
        if professores:
            professores = [professor.strip() for professor in professores]
            professores = [prof for prof in professores if prof != 'MINISTRO']
            professor = ';'.join(professores)
        else:
            professor = ''
        valores = response.xpath(
            '//*[@id="investimento"]/div/div/div/section/div/div/div/div/div/div/div[2]/span[2]/text()').extract()
        if valores:
            valores = [valor.strip() for valor in valores]
        else:
            valor = ''
            valores.append(valor)

        if len(valores) == 2:
            modalidade = 'Híbrido'
        else:
            modalidade = 'Presencial'

        for _, valor in enumerate(valores):
            yield {
                'Empresa': con_treinamentos,
                'Curso': nome_curso,
                'Tipo': tipo_evento,
                'url': response.url,
                'Professor': professor.strip(),
                'Data': data_congresso,
                'Local': local_congresso if local_congresso != '' else 'online',
                'carga-horaria': '',
                'Valor': valor,
            }

