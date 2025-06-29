from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import Config
from models import db, Pontuacao

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

perguntas_por_idioma = {
    "pt": {
        "facil": [
            ["Qual país é conhecido pelo festival das cores chamado Holi?", ["Índia", "China", "Brasil", "Egito"], 0],
            ["Qual país celebra o carnaval com desfiles de escolas de samba?", ["México", "Espanha", "Colômbia", "Brasil"], 3],
            ["Onde se fala principalmente o idioma Espanhol?", ["França", "México", "Itália", "Alemanha"], 1],
            ["Qual país é famoso por sua educação sem provas e foco na criatividade?", ["Finlândia", "Japão", "Estados Unidos", "Índia"], 0],
            ["Qual continente tem a maior diversidade de idiomas?", ["Ásia", "Europa", "África", "América"], 2]
        ],
        "medio": [
            ["Qual idioma tem diferentes níveis de formalidade usados conforme a hierarquia social?", ["Português", "Francês", "Coreano", "Inglês"], 2],
            ["O que é comum em países asiáticos ao entrar em casa?", ["Beijar a porta", "Tirar os sapatos", "Bater palmas", "Oferecer chá"], 1],
            ["Qual país tem universidades públicas gratuitas e bem avaliadas mundialmente?", ["Estados Unidos", "Alemanha", "Brasil", "Japão"], 1],
            ["Qual desses países possui mais de um idioma oficial?", ["Argentina", "Canadá", "Itália", "Egito"], 1],
            ["No Japão, que prática cultural acontece em abril e envolve flores de cerejeira?", ["Hanami", "Sakura", "Obon", "Setsubun"], 0]
        ],
        "dificil": [
            ["Quantos idiomas oficiais existem na África do Sul?", ["3", "5", "7", "11"], 3],
            ["Qual país aboliu provas obrigatórias para entrada em universidades em 2004?", ["Alemanha", "França", "Suécia", "Noruega"], 2],
            ["Que tradição ocorre na Índia quando alguém visita uma casa?", ["Abraço coletivo", "Dar doces", "Toque nos pés dos mais velhos", "Cantar"], 2],
            ["Em qual país a língua basca é falada, mesmo não sendo relacionada a nenhuma outra língua europeia?", ["Itália", "França", "Espanha", "Grécia"], 2],
            ["Qual país tem o sistema educacional mais longo em média (anos de estudo)?", ["Coreia do Sul", "Estados Unidos", "Austrália", "Noruega"], 0]
        ]
    },
    "en": {
        "facil": [
            ["Which country is known for the colorful festival called Holi?", ["India", "China", "Brazil", "Egypt"], 0],
            ["Which country celebrates carnival with samba school parades?", ["Mexico", "Spain", "Colombia", "Brazil"], 3],
            ["Where is the Spanish language mainly spoken?", ["France", "Mexico", "Italy", "Germany"], 1],
            ["Which country is famous for its education without exams and focus on creativity?", ["Finland", "Japan", "United States", "India"], 0],
            ["Which continent has the greatest diversity of languages?", ["Asia", "Europe", "Africa", "America"], 2]
        ],
        "medio": [
            ["Which language has different levels of formality used according to social hierarchy?", ["Portuguese", "French", "Korean", "English"], 2],
            ["What is common in Asian countries when entering a house?", ["Kissing the door", "Taking off shoes", "Clapping hands", "Offering tea"], 1],
            ["Which country has free and highly-rated public universities worldwide?", ["United States", "Germany", "Brazil", "Japan"], 1],
            ["Which of these countries has more than one official language?", ["Argentina", "Canada", "Italy", "Egypt"], 1],
            ["In Japan, which cultural practice takes place in April and involves cherry blossoms?", ["Hanami", "Sakura", "Obon", "Setsubun"], 0]
        ],
        "dificil": [
            ["How many official languages are there in South Africa?", ["3", "5", "7", "11"], 3],
            ["Which country abolished mandatory university entrance exams in 2004?", ["Germany", "France", "Sweden", "Norway"], 2],
            ["What tradition occurs in India when someone visits a house?", ["Collective hug", "Giving sweets", "Touching the feet of elders", "Singing"], 2],
            ["In which country is the Basque language spoken, even though it is not related to any other European language?", ["Italy", "France", "Spain", "Greece"], 2],
            ["Which country has the longest average educational system (years of study)?", ["South Korea", "United States", "Australia", "Noruega"], 0]
        ]
    },
    "es": {
        "facil": [
            ["¿Qué país es conocido por el festival de los colores llamado Holi?", ["India", "China", "Brasil", "Egipto"], 0],
            ["¿Qué país celebra el carnaval con desfiles de escuelas de samba?", ["México", "España", "Colombia", "Brasil"], 3],
            ["¿Dónde se habla principalmente el idioma español?", ["Francia", "México", "Italia", "Alemania"], 1],
            ["¿Qué país es famoso por su educación sin exámenes y enfoque en la creatividad?", ["Finlandia", "Japón", "Estados Unidos", "India"], 0],
            ["¿Qué continente tiene la mayor diversidad de idiomas?", ["Asia", "Europa", "África", "América"], 2]
        ],
        "medio": [
            ["¿Qué idioma tiene diferentes niveles de formalidad según la jerarquía social?", ["Portugués", "Francés", "Coreano", "Inglés"], 2],
            ["¿Qué es común en los países asiáticos al entrar en una casa?", ["Besar la puerta", "Quitarse los zapatos", "Aplaudiendo", "Ofrecer té"], 1],
            ["¿Qué país tiene universidades públicas gratuitas y muy bien valoradas a nivel mundial?", ["Estados Unidos", "Alemania", "Brasil", "Japón"], 1],
            ["¿Cuál de estos países tiene más de un idioma oficial?", ["Argentina", "Canadá", "Itália", "Egipto"], 1],
            ["En Japón, ¿qué práctica cultural se celebra en abril y se asocia con las flores de cerezo?", ["Hanami", "Sakura", "Obon", "Setsubun"], 0]
        ],
        "dificil": [
            ["¿Cuántos idiomas oficiales hay en Sudáfrica?", ["3", "5", "7", "11"], 3],
            ["¿Qué país abolió los exámenes de ingreso obligatorios a la universidad en 2004?", ["Alemania", "Francia", "Suecia", "Noruega"], 2],
            ["¿Qué tradición ocurre en la India cuando alguien visita una casa?", ["Abrazo colectivo", "Dar dulces", "Tocar los pies de los mayores", "Cantar"], 2],
            ["¿En qué país se habla el idioma vasco, aunque no esté relacionado con ninguna otra lengua europea?", ["Itália", "Francia", "España", "Grecia"], 2],
            ["¿Qué país tiene el sistema educativo más largo en promedio (años de estudio)?", ["Corea del Sur", "Estados Unidos", "Australia", "Noruega"], 0]
        ]
    },
    "fr": {
        "facil": [
            ["Quel pays est connu pour le festival des couleurs appelé Holi?", ["Inde", "Chine", "Brésil", "Égypte"], 0],
            ["Quel pays célèbre le carnaval avec des défilés d'écoles de samba?", ["Mexique", "Espagne", "Colombie", "Brésil"], 3],
            ["Où parle-t-on principalement l'espagnol?", ["France", "Mexique", "Italie", "Allemagne"], 1],
            ["Quel pays est célèbre pour son éducation sans examens et axée sur la créativité?", ["Finlande", "Japon", "États-Unis", "Inde"], 0],
            ["Quel continent a la plus grande diversité de langues?", ["Asie", "Europe", "Afrique", "Amérique"], 2]
        ],
        "medio": [
            ["Quelle langue a différents niveaux de formalité utilisés selon la hiérarchie sociale?", ["Portugais", "Français", "Coréen", "Anglais"], 2],
            ["Qu'est-ce qui est courant dans les pays asiatiques en entrant dans une maison?", ["Embrasser la porte", "Enlever ses chaussures", "Applaudir", "Offrir du thé"], 1],
            ["Quel pays a des universités publiques gratuites et très bien classées dans le monde?", ["États-Unis", "Allemagne", "Brésil", "Japon"], 1],
            ["Lequel de ces pays a plus d'une langue officielle?", ["Argentine", "Canada", "Italie", "Égypte"], 1],
            ["Au Japon, quelle pratique culturelle a lieu en avril et implique les fleurs de cerisier?", ["Hanami", "Sakura", "Obon", "Setsubun"], 0]
        ],
        "dificil": [
            ["Combien de langues officielles y a-t-il en Afrique du Sud?", ["3", "5", "7", "11"], 3],
            ["Quel pays a aboli les examens d'entrée obligatoires à l'université en 2004?", ["Allemagne", "France", "Suède", "Norvège"], 2],
            ["Quelle tradition a lieu en Inde quand quelqu'un visite une maison?", ["Câlin collectif", "Donner des bonbons", "Toucher les pieds des aînés", "Chanter"], 2],
            ["Dans quel pays la langue basque est-elle parlée, même si elle n'est liée à aucune autre langue européenne?", ["Italie", "France", "Espagne", "Grèce"], 2],
            ["Quel pays a le système éducatif moyen le plus long (années d'études)?", ["Corée du Sud", "États-Unis", "Australie", "Norvège"], 0]
        ]
    },
    "it": {
        "facil": [
            ["Quale paese è conosciuto per il festival dei colori chiamato Holi?", ["India", "Cina", "Brasile", "Egitto"], 0],
            ["Quale paese celebra il carnevale con sfilate di scuole di samba?", ["Messico", "Spagna", "Colombia", "Brasile"], 3],
            ["Dove si parla principalmente lo spagnolo?", ["Francia", "Messico", "Italia", "Germania"], 1],
            ["Quale paese è famoso per la sua istruzione senza esami e focalizzata sulla creatività?", ["Finlandia", "Giappone", "Stati Uniti", "India"], 0],
            ["Quale continente ha la maggiore diversità di lingue?", ["Asia", "Europa", "Africa", "America"], 2]
        ],
        "medio": [
            ["Quale lingua ha diversi livelli di formalità usati in base alla gerarchia sociale?", ["Portoghese", "Francese", "Coreano", "Inglese"], 2],
            ["Cosa è comune nei paesi asiatici quando si entra in una casa?", ["Baciare la porta", "Togliersi le scarpe", "Battere le mani", "Offrire il tè"], 1],
            ["Quale paese ha università pubbliche gratuite e molto apprezzate a livello mondiale?", ["Stati Uniti", "Germania", "Brasile", "Giappone"], 1],
            ["Quale di questi paesi ha più di una lingua ufficiale?", ["Argentina", "Canada", "Italia", "Egitto"], 1],
            ["In Giappone, quale pratica culturale si svolge ad aprile e coinvolge i fiori di ciliegio?", ["Hanami", "Sakura", "Obon", "Setsubun"], 0]
        ],
        "dificil": [
            ["Quante lingue ufficiali ci sono in Sudafrica?", ["3", "5", "7", "11"], 3],
            ["Quale paese ha abolito gli esami di ammissione universitari obbligatori nel 2004?", ["Germania", "Francia", "Svezia", "Norvegia"], 2],
            ["Quale tradizione si verifica in India quando qualcuno visita una casa?", ["Abbraccio collettivo", "Dare dolci", "Toccare i piedi degli anziani", "Cantare"], 2],
            ["In quale paese si parla la lingua basca, anche se non è correlata a nessun'altra lingua europea?", ["Italia", "Francia", "Spagna", "Grecia"], 2],
            ["Quale paese ha il sistema educativo medio più lungo (anni di studio)?", ["Corea del Sud", "Stati Uniti", "Australia", "Norvegia"], 0]
        ]
    }
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz/<nivel>')
def quiz(nivel):
    idioma_selecionado = request.args.get('lang', 'pt')

    if idioma_selecionado not in perguntas_por_idioma:
        idioma_selecionado = 'pt'

    if nivel not in perguntas_por_idioma[idioma_selecionado]:
        idioma_selecionado = 'pt'
        if nivel not in perguntas_por_idioma[idioma_selecionado]:
            return "Nível não encontrado para o idioma padrão!", 404


    perguntas_do_nivel = perguntas_por_idioma[idioma_selecionado][nivel]
    return render_template('quiz.html', nivel=nivel, perguntas=perguntas_do_nivel, current_lang=idioma_selecionado)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    nome_jogador = data['nome']
    respostas = data['respostas']
    nivel = data['nivel']
    lang_submitted = data.get('lang', 'pt')

    perguntas_do_nivel_para_pontuacao = perguntas_por_idioma.get(lang_submitted, perguntas_por_idioma['pt'])[nivel]

    acertos = 0
    for i, pergunta_info in enumerate(perguntas_do_nivel_para_pontuacao):
        resposta_correta_idx = pergunta_info[2]
        if i < len(respostas) and respostas[i] == resposta_correta_idx:
            acertos += 1

    nova_pontuacao = Pontuacao(
        nome_jogador=nome_jogador,
        nivel=nivel,
        pontos=acertos
    )
    db.session.add(nova_pontuacao)
    db.session.commit()

    return jsonify({'acertos': acertos, 'total': len(perguntas_do_nivel_para_pontuacao)})

@app.route('/ranking')
def ranking():
    limite_ranking = 10

    ranking_facil = Pontuacao.query.filter_by(nivel='facil').order_by(Pontuacao.pontos.desc()).limit(limite_ranking).all()
    ranking_medio = Pontuacao.query.filter_by(nivel='medio').order_by(Pontuacao.pontos.desc()).limit(limite_ranking).all()
    ranking_dificil = Pontuacao.query.filter_by(nivel='dificil').order_by(Pontuacao.pontos.desc()).limit(limite_ranking).all()

    return render_template(
        'ranking.html',
        ranking_facil=ranking_facil,
        ranking_medio=ranking_medio,
        ranking_dificil=ranking_dificil
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)