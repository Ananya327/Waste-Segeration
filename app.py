
import streamlit as st
from PIL import Image
import settings
import helper

st.set_page_config(
    page_title="Waste Classification using YOLOv8",
    page_icon="♻️",
    layout="wide"
)

st.title("Waste Classification using YOLOv8")


# --------------------------------------------------
# GREEN ADVISER KNOWLEDGE BASE
# --------------------------------------------------

GREEN_ADVISER = {

    "plastic": {
        "name": "Plastic Waste",
        "action": (
            "Clean plastic containers before recycling and separate "
            "plastic waste properly. Send accepted plastic materials "
            "to authorized recycling facilities."
        ),
        "tip": (
            "Plastic can be converted into fibres and construction materials."
        ),
        "environment": (
            "Plastic takes hundreds of years to decompose. "
            "Plastic pollution harms marine life and contaminates "
            "the natural environment."
        ),
        "health": (
            "Burning plastic releases toxic gases that may cause "
            "asthma and lung diseases. Microplastics can also "
            "contaminate food and drinking water."
        )
    },

    "glass": {
        "name": "Glass Waste",
        "action": (
            "Wash glass bottles before recycling and place them "
            "in designated glass recycling bins. Handle broken "
            "glass carefully and keep it in a secure container."
        ),
        "tip": (
            "Glass can be recycled repeatedly without losing its quality."
        ),
        "environment": (
            "Glass in landfills can remain for thousands of years. "
            "Recycling glass reduces landfill waste and the need "
            "for new raw materials."
        ),
        "health": (
            "Broken glass can cause deep cuts and injuries. "
            "Improperly treated wounds may develop infections, "
            "including tetanus."
        )
    },

    "metal": {
        "name": "Metal Waste",
        "action": (
            "Separate metal cans and other recyclable metal items. "
            "Send them to authorized scrap dealers or metal recycling centres."
        ),
        "tip": (
            "Recycling aluminium can save up to 95% of the energy "
            "required to produce it from raw materials."
        ),
        "environment": (
            "Mining metals damages ecosystems, destroys natural habitats "
            "and increases environmental pollution."
        ),
        "health": (
            "Sharp metal edges can cause injuries. Rusty or contaminated "
            "metal objects can create infection risks, including tetanus "
            "through contaminated wounds."
        )
    },

    "organic": {
        "name": "Food / Organic Waste",
        "action": (
            "Compost vegetable peels, fruit waste and suitable food "
            "leftovers. Use a home compost bin or an authorized "
            "organic waste collection facility."
        ),
        "tip": (
            "Compost can be used as natural fertilizer for plants and gardens."
        ),
        "environment": (
            "Organic waste produces methane gas when it decomposes "
            "in landfills. Methane contributes to climate change."
        ),
        "health": (
            "Rotting food waste attracts flies, pests and harmful bacteria. "
            "Poor waste management can contribute to the spread of "
            "diseases such as cholera and typhoid."
        )
    },

    "paper": {
        "name": "Paper Waste",
        "action": (
            "Place paper in recycling bins. Keep paper clean and dry. "
            "Separate recyclable paper from food-contaminated waste."
        ),
        "tip": (
            "Recycled paper can be used to manufacture new cartons, "
            "books and other paper products."
        ),
        "environment": (
            "Excessive paper consumption increases the demand for trees "
            "and contributes to deforestation."
        ),
        "health": (
            "Burning paper releases smoke and fine particles that "
            "may cause asthma and breathing problems."
        )
    },

    "electronic": {
        "name": "Electronic Waste",
        "action": (
            "Do not throw electronic waste into normal dustbins. "
            "Take old electronic devices to an authorized e-waste "
            "collection centre or registered recycler. Some electronic "
            "stores also accept old batteries."
        ),
        "tip": (
            "Electronic devices contain valuable materials such as "
            "copper and gold that can be recovered through recycling."
        ),
        "environment": (
            "Toxic substances such as lead and mercury can contaminate "
            "soil and water when electronic waste is improperly discarded."
        ),
        "health": (
            "Unsafe handling of e-waste may cause nervous system damage, "
            "breathing problems and skin irritation. Long-term exposure "
            "to certain hazardous substances may increase cancer risk."
        )
    },

    "cloth": {
        "name": "Cloth / Textile Waste",
        "action": (
            "Reuse old clothes, donate wearable garments and separate "
            "unusable textiles for collection through textile recycling "
            "programmes."
        ),
        "tip": (
            "Old textiles can be converted into cleaning cloths, "
            "insulation materials and recycled textile fibres."
        ),
        "environment": (
            "Discarded textiles increase landfill waste. Synthetic fabrics "
            "can release microfibres into the environment."
        ),
        "health": (
            "Damp textile waste can encourage mould growth and may "
            "cause skin irritation or respiratory discomfort."
        )
    },

    "shoes": {
        "name": "Footwear Waste",
        "action": (
            "Donate usable shoes, repair damaged footwear where possible "
            "and send unusable shoes to appropriate footwear recycling "
            "or collection programmes."
        ),
        "tip": (
            "Some footwear materials, including rubber and certain plastics, "
            "can be recovered and reused in new products."
        ),
        "environment": (
            "Discarded shoes can remain in landfills for long periods "
            "because they contain mixed materials such as rubber, foam "
            "and synthetic plastics."
        ),
        "health": (
            "Improperly discarded footwear can collect stagnant water "
            "and attract insects and pests. Accumulated waste can "
            "also create unhygienic surroundings."
        )
    }
}





# --------------------------------------------------
# MATCH YOLO CLASS NAMES TO GREEN ADVISER CATEGORIES
# --------------------------------------------------

def normalize_category(label):
    label = (
        label.lower()
        .strip()
        .replace("_", " ")
        .replace("-", " ")
    )

    aliases = {
    "plastic": "plastic",
    "plastic waste": "plastic",
    "trash": "plastic",

    "glass": "glass",
    "glass waste": "glass",

    "organic": "organic",
    "organic waste": "organic",
    "biological": "organic",
    "biodegradable": "organic",

    "paper": "paper",
    "paper waste": "paper",
    "cardboard": "paper",

    "electronic": "electronic",
    "electronics": "electronic",
    "electronic waste": "electronic",
    "e waste": "electronic",
    "battery": "electronic",

    "metal": "metal",
    "metal waste": "metal"
}
    return aliases.get(label)


# --------------------------------------------------
# GREEN ADVISER DISPLAY
# --------------------------------------------------





def display_green_adviser(category):

    advice = GREEN_ADVISER[category]

    html_code = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: white;
            margin: 0;
            padding: 5px;
        }}

        .green-adviser-card {{
            background-color: #ffffff;
            border-left: 5px solid #23833d;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.10);
        }}

        .green-adviser-title {{
            color: #176b2c;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 14px;
        }}

        .green-adviser-content {{
            color: #333333;
            font-size: 14px;
            line-height: 1.8;
        }}

        .green-adviser-content b {{
            color: #222222;
        }}
    </style>
    </head>

    <body>
        <div class="green-adviser-card">

            <div class="green-adviser-title">
                ♻️ {advice['name']} Detected
            </div>

            <div class="green-adviser-content">

                <b>Recommended Action:</b>
                {advice['action']}<br>

                <b>Recycling Tip:</b>
                {advice['tip']}<br>

                <b>Environmental Impact:</b>
                {advice['environment']}<br>

                <b>Health Risks:</b>
                {advice['health']}

            </div>
        </div>
    </body>
    </html>
    """

    st.components.v1.html(
        html_code,
        height=280,
        scrolling=True
    )



    
# --------------------------------------------------
# LOAD YOLOv8 MODEL
# --------------------------------------------------

st.sidebar.header("ML Model Config")

confidence = st.sidebar.slider(
    "Model Confidence",
    min_value=25,
    max_value=100,
    value=40
) / 100

try:
    model = helper.load_model(settings.DETECTION_MODEL)
    st.sidebar.success("YOLOv8 model loaded successfully")

except Exception as e:
    st.error("YOLOv8 model failed to load.")
    st.error(str(e))
    st.stop()


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

st.sidebar.header("Image Config")

uploaded_file = st.sidebar.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

col1, col2 = st.columns(2)

image = None

with col1:
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
            # width=250
        )
    else:
        st.image(
            settings.DEFAULT_IMAGE,
            caption="Default Image",
            use_container_width=True
            #width=250
        )


# --------------------------------------------------
# DETECTION AND GREEN ADVISER RESULTS
# --------------------------------------------------

with col2:
    if uploaded_file is not None:
        detect_clicked = st.button(
            "Detect Objects",
            type="primary"
        )

        if detect_clicked:
            with st.spinner("Detecting waste..."):
                results = model.predict(
                    source=image,
                    conf=confidence,
                    verbose=False
                )

            result = results[0]

            # Display annotated detection image
            annotated_image = result.plot()

            st.image(
                annotated_image,
                caption="Detected Image",
                channels="BGR",
                use_container_width=True
              # width=250
                
            )

            # Extract recognized waste categories
            detected_categories = set()

            if result.boxes is not None and len(result.boxes) > 0:

                for class_id in result.boxes.cls.tolist():
                    label = result.names[int(class_id)]
                    category = normalize_category(label)
                    if category:
                        detected_categories.add(category)
                        
                   

                # Green Adviser section
                st.markdown("---")
                st.markdown(
                    "<h3 style='color:#16803c;'>"
                    "🌱 Green Adviser"
                    "</h3>",
                    unsafe_allow_html=True
                )

                if detected_categories:
                    for category in sorted(detected_categories):
                        display_green_adviser(category)

                else:
                    st.warning(
                        "Waste detected, but the class name does not "
                        "match a Green Adviser category. Check the "
                        "class names in your data.yaml file."
                    )

            else:
                st.warning(
                    "No waste objects detected. Try another image "
                    "or lower the confidence threshold."
                )

    else:
        st.info(
            "Upload an image from the sidebar and click "
            "'Detect Objects' to view the Green Adviser."
        )
