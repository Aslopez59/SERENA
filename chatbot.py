# Palabras que indican crisis o riesgo — activan mensaje de ayuda inmediata
PALABRAS_CRISIS = [
    "suicidio", "suicidarme", "suicidarme", "suicida", "suicidar",
    "muerte", "morir", "matarme", "quitarme la vida", "acabar con todo",
    "no quiero vivir", "no quiero seguir", "hacerme daño", "hacerme daño",
    "autolesión", "autolesionarme", "cortarme", "lastimarme",
    "quisiera morir", "mejor estar muerto", "desaparecer para siempre",
    "terminar con mi vida", "fin de mi vida", "ya no puedo más"
]

MENSAJE_CRISIS = (
    "⚠️ Lo que describes me preocupa mucho y quiero que sepas que no estás solo/a. "
    "Por favor, no te hagas daño. Tu vida tiene un valor enorme.\n\n"
    "🆘 Contacta de inmediato a:\n"
    "• Bienestar Universitario UCatólica: dirígete personalmente o usa el apartado 'Bienestar' en esta app.\n"
    "• Línea 106 – Línea de Salud Mental (Colombia, gratuita, 24 horas).\n"
    "• Línea 123 – Emergencias.\n\n"
    "Por favor busca ayuda ahora. Hay personas que quieren apoyarte."
)


def contiene_palabra_crisis(texto: str) -> bool:
    texto_lower = texto.lower()
    for palabra in PALABRAS_CRISIS:
        if palabra in texto_lower:
            return True
    return False


def responder_chatbot(mensaje: str, estado_animo: str):
    # Primero verificar si el mensaje contiene palabras de crisis
    if contiene_palabra_crisis(mensaje) or contiene_palabra_crisis(estado_animo):
        return MENSAJE_CRISIS

    estado_animo = estado_animo.lower()

    if estado_animo == "triste":
        return (
            "Lamento que te estés sintiendo triste. A veces escribir lo que sentimos ayuda a ordenar los pensamientos. "
            "Puedes intentar respirar profundo, tomar un poco de agua y hablar con alguien de confianza. "
            "Recuerda que no tienes que pasar por esto solo/a.\n\n"
            "💡 Consejo: Sal a caminar aunque sea 10 minutos. El movimiento y el aire fresco pueden hacer "
            "una gran diferencia en cómo te sientes. También puedes escuchar música que te guste o ver algo "
            "que te dé risa. La tristeza es temporal, y mereces sentirte bien."
        )

    elif estado_animo == "ansioso":
        return (
            "Entiendo que la ansiedad puede sentirse muy incómoda. Intenta este ejercicio: inhala durante 4 segundos, "
            "mantén el aire 4 segundos y exhala lentamente durante 6 segundos. Repite esto varias veces. "
            "También puede ayudarte enfocarte en algo que puedas ver, tocar o escuchar en este momento.\n\n"
            "💡 Consejo: La técnica 5-4-3-2-1 funciona muy bien para la ansiedad: nombra 5 cosas que puedes ver, "
            "4 que puedes tocar, 3 que puedes escuchar, 2 que puedes oler y 1 que puedes saborear. "
            "Esto le recuerda a tu mente que estás a salvo aquí y ahora."
        )

    elif estado_animo == "estresado":
        return (
            "El estrés suele aparecer cuando sentimos que tenemos muchas cosas encima. Intenta hacer una lista pequeña "
            "con lo más urgente y empieza por una sola tarea. No tienes que resolver todo al mismo tiempo.\n\n"
            "💡 Consejo: Divide tus tareas en bloques de 25 minutos (técnica Pomodoro): trabaja 25 min, descansa 5 min. "
            "Esto evita el agotamiento mental. También recuerda comer bien y dormir suficiente: un cerebro descansado "
            "rinde mucho mejor que uno agotado."
        )

    elif estado_animo == "enojado":
        return (
            "Sentir enojo también es válido. Antes de responder o actuar, intenta alejarte un momento, respirar y pensar "
            "qué fue exactamente lo que te hizo sentir así. Escribirlo puede ayudarte a entender mejor la situación.\n\n"
            "💡 Consejo: Cuando sientas que el enojo sube mucho, cuenta hacia atrás desde 10 en voz baja o en tu mente. "
            "Esto activa la parte racional del cerebro y baja la intensidad de la emoción. "
            "Después, expresa lo que sientes con calma y sin acusaciones, usando frases como 'yo me siento...' en lugar de 'tú me hiciste...'"
        )

    elif estado_animo == "cansado":
        return (
            "El cansancio también afecta cómo pensamos y sentimos. Si puedes, toma una pausa corta, descansa la vista, "
            "hidrátate y trata de dormir mejor hoy. Tu bienestar también necesita espacio.\n\n"
            "💡 Consejo: Revisa tu higiene del sueño: evita pantallas al menos 30 minutos antes de dormir, "
            "intenta acostarte siempre a la misma hora y mantén tu cuarto oscuro y fresco. "
            "Si el cansancio persiste por muchos días, podría ser señal de algo más profundo y vale la pena hablar con alguien."
        )

    elif estado_animo == "confundido":
        return (
            "Sentirse confundido puede pasar cuando hay muchas emociones o decisiones al mismo tiempo. Intenta escribir "
            "qué es lo que te preocupa y separarlo por partes. A veces entender el problema paso a paso lo hace más manejable.\n\n"
            "💡 Consejo: Escribe en una hoja todo lo que tienes en la cabeza sin filtro, luego encierra en un círculo "
            "lo que sí puedes controlar y tacha lo que no. Concéntrate solo en lo que está dentro de tu alcance hoy. "
            "Dar un pequeño paso ya es un avance."
        )

    elif estado_animo == "solo":
        return (
            "Siento que te estés sintiendo solo/a. A veces puede ayudar enviarle un mensaje a alguien de confianza o acercarte "
            "a un espacio de apoyo. También puedes usar el apartado de Bienestar si necesitas hablar con alguien.\n\n"
            "💡 Consejo: La soledad a veces nos lleva a encerrarnos más, pero pequeños gestos sociales ayudan mucho: "
            "saludar a un compañero, unirte a un grupo de estudio o participar en actividades de bienestar universitario. "
            "Recuerda que pedir compañía no es una debilidad, es un acto de valentía."
        )

    elif estado_animo == "feliz":
        return (
            "¡Qué bien que te sientas así! La felicidad también merece ser reconocida y celebrada. "
            "Aprovechar los momentos buenos nos da energía para afrontar los difíciles.\n\n"
            "💡 Consejo: Toma nota de lo que hizo este momento especial. Llevar un diario de gratitud "
            "donde escribas 3 cosas buenas del día, por pequeñas que sean, puede ayudarte a mantener "
            "una perspectiva positiva incluso en los días más complicados."
        )

    elif estado_animo == "nervioso":
        return (
            "Los nervios son una respuesta normal ante situaciones nuevas o importantes. Tu cuerpo está "
            "preparándose para dar lo mejor de sí. No luches contra ellos, acéptalos.\n\n"
            "💡 Consejo: Antes de un examen o presentación, haz respiraciones lentas y recuerda momentos "
            "en que lo lograste. Prepararse bien de antemano es la mejor forma de reducir los nervios. "
            "Y si aun así aparecen, está bien: muchas personas se desempeñan muy bien aunque estén nerviosas."
        )

    elif estado_animo == "desmotivado":
        return (
            "La desmotivación a veces llega cuando no vemos el propósito de lo que hacemos o cuando llevamos "
            "mucho tiempo sin descansar. Es importante escuchar esa señal.\n\n"
            "💡 Consejo: Intenta reconectar con tu 'por qué': ¿qué te llevó a elegir tu carrera? ¿Qué quieres "
            "construir con ella? A veces también ayuda darse un pequeño premio al completar una tarea. "
            "Los logros pequeños también cuentan y merecen reconocimiento."
        )

    elif estado_animo == "agotado":
        return (
            "El agotamiento profundo es diferente al cansancio normal, y tu cuerpo y mente te están pidiendo una pausa. "
            "No ignores esa señal.\n\n"
            "💡 Consejo: Prioriza el descanso activo: no solo dormir, sino actividades que te recarguen de verdad "
            "como caminar, escuchar música, hablar con alguien que te haga reír o pasar tiempo en la naturaleza. "
            "Si el agotamiento lleva muchas semanas, considera hablar con el equipo de Bienestar Universitario."
        )

    elif estado_animo == "crisis":
        return (
            "Siento mucho que estés pasando por un momento tan difícil. Si sientes que estás en riesgo o no puedes manejar "
            "la situación, por favor busca ayuda inmediata con una persona cercana o comunícate con Bienestar Universitario. "
            "También puedes usar el apartado de Bienestar en esta aplicación para enviar una solicitud de apoyo.\n\n"
            "🆘 Línea de crisis: 106 (gratuita, 24 horas) | Emergencias: 123"
        )

    else:
        return (
            "Gracias por compartir cómo te sientes. Reconocer lo que pasa dentro de ti es un primer paso muy valioso. "
            "Puedes intentar respirar con calma, escribir lo que estás sintiendo y buscar apoyo si lo necesitas.\n\n"
            "💡 Recuerda: Serena está aquí para acompañarte. Si en algún momento sientes que necesitas hablar "
            "con alguien del equipo de Bienestar, puedes hacerlo desde el apartado 'Bienestar' de la aplicación. "
            "No estás solo/a en esto."
        )
