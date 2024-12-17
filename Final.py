import streamlit as st
import base64
from datetime import date, datetime, time, timedelta
from fpdf import FPDF  # Librería para generar PDF

# Configurar el diseño de la página
st.set_page_config(page_title="Calculadora de Kahu Nanny")

# Variables para manejar el estado de la aplicación
if 'page' not in st.session_state:
    st.session_state.page = 'calculator'

if 'show_contract_button' not in st.session_state:
    st.session_state.show_contract_button = False

if 'num_kids' not in st.session_state:
    st.session_state.num_kids = 1

if 'ages' not in st.session_state:
    st.session_state.ages = []

if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = []

if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0

if 'service_zone' not in st.session_state:
    st.session_state.service_zone = ""

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if 'end_time' not in st.session_state:
    st.session_state.end_time = None

if 'allergies' not in st.session_state:
    st.session_state.allergies = ""

if 'activities' not in st.session_state:
    st.session_state.activities = ""

# Función para cargar la imagen del logo y convertirla a base64
def load_logo(file_path):
    with open(file_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded

# Cargar el logo
logo_path = "Copy of Logo Kahu (3).png"
logo_base64 = load_logo(logo_path)

# Encabezado con el logo más grande y lema
def show_header():
    st.markdown(
        f"""
         <text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" alt="Kahu Nanny Logo" style="height: 150px; margin-bottom: 10px;">
            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 18px; margin-top: 10px;">
                Tu tranquilidad, nuestra prioridad.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Traducción manual de días y meses al español
DAYS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MONTHS_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio", 
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

# Función para formatear las fechas en español
def format_date(d):
    day_name = DAYS_ES[d.weekday()]  # Obtiene el nombre del día
    month_name = MONTHS_ES[d.month - 1]  # Obtiene el nombre del mes
    return f"{day_name} {d.day} de {month_name}"

# Generar opciones de horarios con intervalos de 30 minutos
def generate_time_options():
    start = time(0, 0)  # Hora inicial: 0:00 AM
    end = time(23, 30)  # Hora final: 11:30 PM
    step = timedelta(minutes=30)
    options = []
    # Ajuste en el bucle
    current = datetime.combine(date.today(), start)
    end_datetime = datetime.combine(date.today(), end)
    while current <= end_datetime:
        options.append(current.time())
        current += step  # Sumar intervalos de 30 minutos
    
    return options
    

# Función para generar un PDF
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Logo de Kahu Nanny
    pdf.image("Copy of Logo Kahu (3).png", x=80, y=10, w=50)  # Centrado y ajustado
    pdf.ln(40)  # Salto de línea después del logo

    # Título estilizado
    pdf.set_font("Arial", style="B", size=16)
    pdf.set_text_color(74, 74, 74)  # Gris oscuro
    pdf.cell(0, 10, "Resumen del Servicio Contratado", ln=True, align="C")
    pdf.ln(10)  # Espacio después del título

    # Color azul del logo (ajustable si tienes otro color exacto)
    azul_logo = (138, 43, 226) #en realidad es morado

    # Sección: Detalles del servicio
    pdf.set_font("Arial", style="B", size=14)
    pdf.set_text_color(*azul_logo)  # Cambiar a azul
    pdf.cell(0, 10, "Detalles del servicio:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)  # Negro para el contenido
    for i, age in enumerate(st.session_state.ages):
        pdf.cell(0, 10, f"- Edad del niño {i+1}: {age} años", ln=True)
    pdf.cell(0, 10, f"- Zona del servicio: {st.session_state.service_zone}", ln=True)
    pdf.cell(0, 10, f"- Horario: {st.session_state.start_time.strftime('%I:%M %p')} a {st.session_state.end_time.strftime('%I:%M %p')}", ln=True)

    # Sección: Días seleccionados
    pdf.set_font("Arial", style="B", size=14)
    pdf.set_text_color(*azul_logo)  # Cambiar a azul
    pdf.cell(0, 10, "Días seleccionados:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)  # Negro para el contenido
    for d in st.session_state.selected_dates:
        pdf.cell(0, 10, f"  - {format_date(d)}", ln=True)

    # Sección: Alergias
    if st.session_state.allergies:
        pdf.set_font("Arial", style="B", size=14)
        pdf.set_text_color(*azul_logo)  # Cambiar a azul
        pdf.cell(0, 10, "Alergias o alimentación especial:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)  # Negro para el contenido
        pdf.multi_cell(0, 10, f"{st.session_state.allergies}")
    
    # Sección: Juegos favoritos
    if st.session_state.activities:
        pdf.set_font("Arial", style="B", size=14)
        pdf.set_text_color(*azul_logo)  # Cambiar a azul
        pdf.cell(0, 10, "Juegos y actividades favoritas:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)  # Negro para el contenido
        pdf.multi_cell(0, 10, f"{st.session_state.activities}")

    # Línea final
    pdf.ln(10)
    pdf.set_draw_color(255, 95, 145)  # Rosa Kahu Nanny
    pdf.set_line_width(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Nota final
    pdf.set_font("Arial", style="I", size=10)
    pdf.set_text_color(74, 74, 74)
    pdf.cell(0, 10, "Gracias por confiar en Kahu Nanny. Tu tranquilidad, nuestra prioridad.", ln=True, align="C")

    # Más información
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(74, 74, 74)
    pdf.cell(0, 10, "Si tienes alguna pregunta, no dudes en contactarnos", ln=True)
    pdf.cell(0, 10, "+52 33 2801 4649", ln=True,)
    return pdf

# Configurar acceso a Google Sheets
def save_to_google_sheets(data):
    # Define el alcance de las APIs (Sheets y Drive)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Autenticación con el archivo credentials.json
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Abre el Google Sheet por su ID
    sheet = client.open_by_key("1UAXDH1DLpv54dXTGOYcgah3j30Xnk3QCpVdgNFl911E")  # Reemplaza con el ID de tu hoja
    worksheet = sheet.sheet1  # Usa la primera hoja del archivo

    # Agrega los datos como una nueva fila
    worksheet.append_row(data)


# Página de calculadora
def calculator_page():
    show_header()
    st.title("Calculadora de costos de niñeras")
    st.write("Completa los datos para calcular el costo semanal de tu servicio.")
    
    # Entrada de datos del cliente
    st.markdown("#### **Tu nombre completo:**")
    name = st.text_input("")
    
    st.markdown("#### **Tipo de servicio que buscas:**")
    service_type = st.radio("", ["Fijo", "Esporádico"]).lower()
    
    st.markdown("#### **¿Por cuántas semanas necesitas el servicio?**")
    weeks = st.number_input("", min_value=1, step=1)
    
    st.markdown("#### **Selecciona los días:**")
    days_selected = st.multiselect(
        "",
        options=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        default=["Lunes"]
    )
    num_days = len(days_selected)
    
    st.markdown("#### **¿Cuántas horas por día necesitas?**")
    hours_per_day = st.number_input("", min_value=3, step=1)
    
    st.markdown("#### **¿Cuántos peques serán?**")
    st.session_state.num_kids = st.selectbox("", [1, 2, 3, 4])

    # Precios por hora
    prices = {
        "fijo_20": 89.00,
        "fijo_25": 80.00,
        "fijo_20_3": 94.00,
        "fijo_25_3": 86.00,
        "fijo_20_4": 104.00,
        "fijo_25_4": 96.00,
        "fijo_1": 95.00,
        "fijo_2": 105.00,
        "fijo_3": 115.00,
        "fijo_4": 125.00,
        "por_hora_1": 118.33,
        "por_hora_2": 128.33,
        "por_hora_3": 138.33,
        "por_hora_4": 148.33,
        "extra_1": 110.00,
        "extra_2": 120.00,
        "extra_3": 130.00,
        "extra_4": 140.00,
    }

    # Función para calcular el costo semanal
    def calculate_cost(service_type, weeks, num_days, hours_per_day, num_kids):
        total_hours = num_days * hours_per_day
        if service_type == "fijo" and weeks >= 3:
            if 20 <= total_hours < 25:
                rate = prices[f"fijo_20_{num_kids}"]
            elif total_hours >= 25:
                rate = prices[f"fijo_25_{num_kids}"]
            else:
                rate = prices[f"fijo_{num_kids}"]
            cost = total_hours * rate
        elif service_type == "fijo":
            rate = prices[f"fijo_{num_kids}"]
            cost = total_hours * rate
        else:
            daily_cost = 0
            if hours_per_day <= 3:
                rate = prices[f"por_hora_{num_kids}"]
                daily_cost = hours_per_day * rate
            else:
                base_cost = 3 * prices[f"por_hora_{num_kids}"]
                extra_hours = hours_per_day - 3
                extra_rate = prices[f"extra_{num_kids}"]
                daily_cost = base_cost + (extra_hours * extra_rate)
            cost = daily_cost * num_days
        return cost

    # Botón para calcular el costo semanal
    if st.button("Calcular costo semanal"):
        if service_type == "fijo" and (weeks < 3 or num_days < 2):
            st.error("¡Ups! Los servicios fijos requieren al menos 3 semanas y 2 días por semana. 😊")
        else:
            st.session_state.total_cost = calculate_cost(service_type, weeks, num_days, hours_per_day, st.session_state.num_kids)
            st.success(f"El costo semanal para {name} es: ${round(st.session_state.total_cost)} MXN")
            st.session_state.show_contract_button = True

 # Recomendaciones de servicios adicionales
        st.markdown("##### **¿Quieres mejorar la experiencia de tus pequeños?**")
        st.info(
            """
            🌟 **Recomendaciones:**
            - **Paquetes especiales:** Obtén un descuento adicional si contratas más de 20 horas a la semana.
            - **Actividades creativas personalizadas:** Contáctanos para agregar opciones como pintura, manualidades o cuentos interactivos.
            """
        )

    # Botón para navegar a la página de contratación
    if st.session_state.show_contract_button:
        if st.button("Contratar servicio"):
            st.session_state.page = 'contract'

# Página de contratación
def contract_page():
    show_header()
    st.title("Formulario de Contratación")

    # Preguntar por el número de teléfono
    st.markdown("### **Número de teléfono:**")
    st.session_state.phone = st.text_input("Ingresa tu número de contacto:")
   
    # Campos dinámicos para las edades de los niños
    st.markdown("#### **Edades de tus peques:**")
    st.session_state.ages = []
    for i in range(st.session_state.num_kids):
        age = st.number_input(f"Edad de tu peque {i+1} (en años):", min_value=0, max_value=17, key=f"age_{i}")
        st.session_state.ages.append(age)
   
    st.markdown("#### **Zona donde se realizará el servicio:**")
    st.session_state.service_zone = st.text_input("")
   
    # Opciones de horario con intervalos de 30 minutos
    st.write("#### Selecciona el horario de inicio y finalización del servicio:")
    time_options = generate_time_options()
    st.session_state.start_time = st.selectbox("Hora de inicio", time_options, format_func=lambda t: t.strftime("%I:%M %p"))
    st.session_state.end_time = st.selectbox("Hora de finalización", time_options, format_func=lambda t: t.strftime("%I:%M %p"))


    # Selector para agregar múltiples fechas
    st.write("#### Selecciona los días específicos del servicio:")
    new_date = st.date_input("Agrega un día:", value=date.today(), key="new_date")
    if st.button("Agregar día"):
        if new_date not in st.session_state.selected_dates:
            st.session_state.selected_dates.append(new_date)
        else:
            st.warning("Este día ya está seleccionado. ¿Quieres elegir otro? 📅")
   
    # Mostrar los días seleccionados
    st.write("#### **Días seleccionados:**")
    if st.session_state.selected_dates:
        for selected_date in st.session_state.selected_dates:
            formatted_date = format_date(selected_date)
            st.write(f"- {formatted_date}")
    else:
        st.write("No hay días seleccionados.")


    # Nuevos campos: Alergias y actividades favoritas
    st.markdown("#### **¿Alguna alergia o alimentación especial de tu(s) peque(s)?**")
    st.session_state.allergies = st.text_area("", placeholder="Escribe aquí cualquier detalle importante")

    st.markdown("#### **Cuéntanos cuáles son sus juegos y actividades favoritas:**")
    st.session_state.activities = st.text_area("", placeholder="Ejemplo: Jugar a la pelota, pintar, leer cuentos, etc.")

    if st.button("Confirmar contratación"):
        if not st.session_state.service_zone or not st.session_state.selected_dates:
            st.error("¡Parece que algo falta! Por favor, completa todos los detalles del servicio. ¡Queremos asegurarnos de que todo sea perfecto! 🍼.")
        else:
            st.success("¡Servicio contratado exitosamente! Por favor ponte en contacto con nosotros.🎉")


            pdf = generate_pdf()
            pdf.output("Resumen_del_Servicio.pdf")


            # Botón para descargar el PDF
            with open("Resumen_del_Servicio.pdf", "rb") as pdf_file:
                pdf_data = pdf_file.read()
                st.download_button(
                    label="Descargar Resumen de tu servicio en PDF",
                    data=pdf_data,
                    file_name="Resumen_del_Servicio.pdf",
                    mime="application/pdf"
                )




    if st.button("Regresar a la calculadora"):
        st.session_state.page = 'calculator'




# Navegación entre páginas
if st.session_state.page == 'calculator':
    calculator_page()
elif st.session_state.page == 'contract':
    contract_page()


