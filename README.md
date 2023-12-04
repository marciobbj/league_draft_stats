# LoL Draft Stats

## Sobre
LoL Draft Stats é uma ferramenta para jogadores de League of Legends. Ela fornece análises detalhadas de matchups e composições de equipe.

## Coleta e Armazenamento de Dados
Utilizamos Scrapy para coletar dados, como Tier, Win Rate, Pick Rate e Ban Rate dos campeões. Estes dados são armazenados em formato JSON.

## Como as estatísticas são calculadas
Avaliação da Força do Campeão: Utilizamos Tier, Win Rate, Pick Rate e Ban Rate para avaliar cada campeão. Estes dados são normalizados e ponderados para gerar uma pontuação total, refletindo a força geral do campeão.

Análise de Matchup: Comparamos dois campeões em cada lane, levando em conta suas forças relativas e suas relações de matchup (vantagens e desvantagens históricas). A probabilidade de vitória é calculada com base nessas pontuações.

Identificação de Matchups Fortes: Analisamos se um campeão tem vantagens significativas sobre outro, ajustando a pontuação total se necessário.
## Testes
Realizei testes utilizando as composições que foram usadas pelas equipes que chegaram às finais do Campeonato Mundial de 2023.

Jogo 1: ![t1xwei](/docs/img/t1_x_wei-1.png "T1_x_wei.png")
Jogo 2: ![t1xwei](/docs/img/t1_x_wei-2.png "T1_x_wei.png")
Jogo 3: ![t1xwei](/docs/img/t1_x_wei-3.png "T1_x_wei.png")
## Cálculo de Composições
Calculamos uma média ponderada das pontuações de cada campeão por lane, considerando matchups fortes e fracos. Isso resulta em uma estimativa da taxa de vitória para cada composição de equipe, permitindo comparações estratégicas lado a lado.

## Funcionalidades
- Análise de matchups individuais.
- Avaliação da força do campeão com base em dados atualizados.
- Estimativas de taxa de vitória para composições de equipe.

## Futuras Implementações
- Estatísticas baseadas em modelos de Machine Learning.
- Ajustes dinâmicos baseados em tendências e atualizações do jogo.

## Licença
GPL (General Public License).