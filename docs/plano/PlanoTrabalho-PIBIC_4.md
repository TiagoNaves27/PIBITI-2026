**Plano de Trabalho**

**Informações do aluno**

**Nome:** Tiago Naves de Oliveira Alves

**E-mail:** tiagonaves2003@gmail.com

**Lattes:** https://lattes.cnpq.br/3493217080906970

**CPF:** 025.314.221-02

**Matrícula:** 251015950

**Telefone:** (61) 98280-4002

**Título:** Desenvolvimento de um sistema automatizado de aquisição (IoT) e análise de dados dos ensaios de cisalhamento direto e triaxial.

**Adequação do Plano de Trabalho**

A resistência ao cisalhamento é uma das propriedades mais importantes dos solos, constituindo parâmetro fundamental em projetos geotécnicos como estabilidade de taludes, fundações, muros de contenção e barragens. Sua determinação em laboratório é realizada principalmente por meio de dois ensaios: o ensaio de cisalhamento direto e o ensaio de compressão triaxial. Ambos geram um grande volume de dados (força, deslocamento, deformação e, no caso do triaxial, poropressão e pressão confinante), que tradicionalmente são coletados e processados de forma manual ou semimanual, em planilhas eletrônicas. Esse processo é demorado, sujeito a erros de leitura e transcrição e dificulta a padronização e a reprodutibilidade dos resultados. Com o avanço da Internet das Coisas (IoT) e das ferramentas computacionais, torna-se viável automatizar tanto a aquisição quanto a análise desses dados, permitindo a avaliação dos resultados em tempo real e a redução da intervenção manual.

Desta forma, desenvolveu-se o presente trabalho com o objetivo de desenvolver um aplicativo desktop, em linguagem Python, integrado a um sistema de aquisição automática de dados baseado em Raspberry Pi (IoT), capaz de coletar, armazenar e processar os dados provenientes dos ensaios de cisalhamento direto e triaxial, gerando automaticamente os parâmetros de resistência ao cisalhamento (coesão e ângulo de atrito) e as respectivas representações gráficas. Como objetivos específicos deste projeto, têm-se:

* Introduzir o aluno ao meio científico, dando a ele diretrizes na busca de técnicas e no desenvolvimento de soluções computacionais aplicadas à geotecnia experimental;

* Realizar extensa revisão bibliográfica sobre a resistência ao cisalhamento dos solos, os ensaios de cisalhamento direto e triaxial e os sistemas de aquisição automática de dados baseados em IoT e em Raspberry Pi;

* Desenvolver o sistema de aquisição automática de dados, integrando os sensores das máquinas de ensaio (célula de carga, transdutores de deslocamento e de pressão/poropressão) a um Raspberry Pi, com as rotinas de leitura programadas em Python;

* Estruturar um banco de dados para o armazenamento automático dos dados coletados durante os ensaios;

* Desenvolver, em linguagem Python, o aplicativo desktop de processamento e análise, capaz de calcular as tensões, traçar as curvas características de cada ensaio, construir a envoltória de ruptura de Mohr-Coulomb e determinar a coesão (c) e o ângulo de atrito (φ);

* Avaliar a eficiência do sistema proposto, comparando os resultados obtidos de forma automática com aqueles obtidos pelo processamento manual tradicional dos mesmos ensaios.

**Metodologia da Pesquisa**

As atividades de pesquisa a serem realizadas no presente projeto envolvem os estudos detalhados a seguir, são eles:

* Exposição semanal, por parte do aluno ao professor, do andamento da pesquisa e das dificuldades encontradas, objetivando o crescimento contínuo e permitindo a redefinição das diretrizes da pesquisa sempre que houver necessidade;

* Realização de revisão bibliográfica sobre os ensaios de cisalhamento direto e triaxial, os parâmetros de resistência ao cisalhamento dos solos e os sistemas de aquisição de dados baseados em Raspberry Pi e IoT;

* Desenvolvimento do módulo de aquisição: integração dos sensores das máquinas de ensaio (célula de carga, transdutores de deslocamento e de pressão/poropressão) a um Raspberry Pi, com as rotinas de leitura programadas em linguagem Python;

* Desenvolvimento das rotinas de envio e estruturação do banco de dados em MySQL, para o armazenamento automático dos dados coletados;

* Desenvolvimento do aplicativo desktop em Python, contemplando: o cálculo das tensões normais e cisalhantes; a geração das curvas tensão × deformação e tensão cisalhante × deslocamento; a construção da envoltória de ruptura de Mohr-Coulomb; a determinação da coesão (c) e do ângulo de atrito (φ); e o traçado dos círculos de Mohr para o ensaio triaxial;

* Realização de ensaios de cisalhamento direto e triaxial em laboratório, para a geração dos dados experimentais e o teste do sistema desenvolvido;

* Validação do sistema, por meio da comparação entre os resultados obtidos automaticamente e aqueles obtidos pelo processamento manual tradicional dos mesmos ensaios, aplicando-se a estatística descritiva;

* Desenvolvimento de tabelas, gráficos e registros fotográficos, documentando todo o procedimento e os resultados obtidos;

* Apresentação de seminário para conhecimento da pesquisa por parte de outros alunos da linha de pesquisa do professor, promovendo a interação e a troca de conhecimentos com o grupo;

* Construção de um artigo científico apresentando a relevância prática do sistema desenvolvido no estudo do comportamento mecânico dos solos.

Este trabalho fará parte da linha de pesquisa \[a ser definida pelo Prof. André Luís Brasil Cavalcante\] do GeoFluxo, da Universidade de Brasília, vinculado ao Diretório dos Grupos de Pesquisa no Brasil/CNPq. O desenvolvimento desta pesquisa de iniciação científica colaborará para o ingresso do discente no ambiente de pesquisa e na produção de trabalhos científicos, integrando conhecimentos de geotecnia experimental, programação e automação, uma combinação de grande relevância para a modernização dos ensaios laboratoriais, tanto em âmbito nacional quanto internacional. Desta forma, espera-se a familiarização do discente com as técnicas laboratoriais e com as ferramentas computacionais para a aquisição, o armazenamento e a análise de dados em geotecnia.

**Bibliografia**

AMERICAN SOCIETY FOR TESTING AND MATERIALS (ASTM). *D3080: Standard Test Method for Direct Shear Test of Soils Under Consolidated Drained Conditions.* West Conshohocken, PA.

AMERICAN SOCIETY FOR TESTING AND MATERIALS (ASTM). *D2850: Standard Test Method for Unconsolidated-Undrained Triaxial Compression Test on Cohesive Soils.* West Conshohocken, PA.

AMERICAN SOCIETY FOR TESTING AND MATERIALS (ASTM). *D4767: Standard Test Method for Consolidated Undrained Triaxial Compression Test for Cohesive Soils.* West Conshohocken, PA.

AMERICAN SOCIETY FOR TESTING AND MATERIALS (ASTM). *D7181: Standard Test Method for Consolidated Drained Triaxial Compression Test for Soils.* West Conshohocken, PA.

BISHOP, A. W.; HENKEL, D. J. *The Measurement of Soil Properties in the Triaxial Test.* London: Edward Arnold, 1962\.

HEAD, K. H. *Manual of Soil Laboratory Testing.* Vols. 2 e 3\.

PINTO, Carlos de Sousa. *Curso Básico de Mecânica dos Solos.* São Paulo: Oficina de Textos.

DAS, Braja M. *Fundamentos de Engenharia Geotécnica.* São Paulo: Cengage Learning.

LAMBE, T. W.; WHITMAN, R. V. *Soil Mechanics.* New York: John Wiley & Sons, 1969\.

ATKINSON, J. *The Mechanics of Soils and Foundations.* 2\. ed. London: Taylor & Francis, 2007\.

MONK, Simon. *Programming the Raspberry Pi: Getting Started with Python.* McGraw-Hill Education.

UPTON, E.; HALFACREE, G. *Raspberry Pi User Guide.* Wiley.

POWERS, Philip S. *A microcomputer-based data acquisition and control system for the direct shear, ring shear, triaxial shear, and consolidation tests.* Reston: U.S. Geological Survey, 1983\. (Open-File Report 83-491). DOI: 10.3133/ofr83491.

**Justificativa elaborada:**

O aluno possui bom desempenho acadêmico (IRA 3,8235). Participa do grupo de extensão GeoFluxo (Grupo de Pesquisa Inovações e Tecnologias Aplicadas em Geotecnia Ambiental). Possui experiência em ensaios geotécnicos e em programação, com domínio da linguagem Python e do sistema de gerenciamento de banco de dados MySQL, competências diretamente alinhadas ao desenvolvimento proposto neste plano de trabalho, que envolve a aquisição automática, o armazenamento e a análise de dados de ensaios. Demonstra comprovado interesse em atividades laboratoriais na área de Geotecnia e em seu desenvolvimento acadêmico.

**Cronograma**

| Mês | Atividade |
| :---: | ----- |
| 1 | Revisão bibliográfica sobre resistência ao cisalhamento, ensaios de cisalhamento direto e triaxial e sistemas de aquisição de dados (IoT / Raspberry Pi). Levantamento dos sensores disponíveis nas máquinas de ensaio. |
| 2 | Definição da arquitetura do sistema (sensores → Raspberry Pi → banco de dados → aplicativo). Início da montagem do hardware de aquisição. |
| 3 | Desenvolvimento e teste do módulo de aquisição: leitura dos sensores pelo Raspberry Pi em Python e calibração dos transdutores. |
| 4 | Desenvolvimento das rotinas de envio e estruturação do banco de dados em MySQL. Testes de comunicação e de armazenamento automático dos dados. |
| 5 | Início do desenvolvimento do aplicativo desktop em Python: interface e leitura dos dados a partir do banco. |
| 6 | Implementação dos cálculos: tensões normais e cisalhantes; curvas tensão × deformação e tensão cisalhante × deslocamento. |
| 7 | Implementação da envoltória de Mohr-Coulomb, determinação da coesão (c) e do ângulo de atrito (φ) e traçado dos círculos de Mohr para o triaxial. |
| 8 | Realização dos ensaios de cisalhamento direto e triaxial em laboratório, coletando os dados pelo sistema desenvolvido. |
| 9 | Validação do sistema: comparação dos resultados automáticos com o processamento manual tradicional, aplicando estatística descritiva. |
| 10 | Ajustes finais no sistema e apresentação do relatório de acompanhamento. |
| 11 | Redação do artigo científico. |
| 12 | Redação do trabalho final e apresentação em congresso/seminário. |

&nbsp;