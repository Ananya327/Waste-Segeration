
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
            "Separate plastic waste and send it to an appropriate "
            "recycling facility if accepted. Do not burn plastic."
        ),
        "environment": (
            "Improper disposal contributes to long-lasting pollution, "
            "harms wildlife, and can generate microplastics."
        ),
        "health": (
            "Burning plastic can release harmful fumes. Improperly "
            "discarded plastic can create hazards for animals and people."
        )
    },

    "glass": {
        "name": "Glass Waste",
        "action": (
            "Recycle clean glass containers where accepted. Place broken "
            "glass in a secure, clearly marked container."
        ),
        "environment": (
            "Recycling glass reduces landfill waste and the need for "
            "new raw materials."
        ),
        "health": "Broken glass can cause cuts and injuries."
    },

    "organic": {
        "name": "Organic Waste",
        "action": (
            "Compost suitable food scraps and plant waste at home "
            "or through an authorized composting facility."
        ),
        "environment": (
            "Composting returns nutrients to the soil. Organic waste "
            "in landfills can generate methane during decomposition."
        ),
        "health": (
            "Poorly managed organic waste can attract pests "
            "and produce unpleasant odours."
        )
    },

    "paper": {
        "name": "Paper Waste",
        "action": (
            "Keep paper clean and dry and send recyclable paper for "
            "recycling. Avoid mixing it with food-contaminated "
            "or heavily soiled waste."
        ),
        "environment": (
            "Recycling can reduce the demand for virgin wood, "
            "water, and energy."
        ),
        "health": (
            "Damp or mouldy paper may contribute to respiratory "
            "irritation in sensitive individuals."
        )
    },

    "electronic": {
        "name": "Electronic Waste",
        "action": (
            "Send electronic waste to an authorized collection centre "
            "or registered recycler. Avoid burning or informally "
            "dismantling electronic devices."
        ),
        "environment": (
            "Improper handling can contaminate soil, water, and air "
            "and waste recoverable materials."
        ),
        "health": (
            "Unsafe dismantling or processing may expose people "
            "to hazardous substances and toxic metals."
        )
    },

    "metal": {
        "name": "Metal Waste",
        "action": (
            "Separate recyclable metal and send it to an appropriate "
            "scrap dealer or recycling facility. Handle sharp edges carefully."
        ),
        "environment": (
            "Recycling conserves mineral resources and can reduce the "
            "energy needed to produce metal from raw materials."
        ),
        "health": (
            "Sharp edges can cause cuts. Coated or contaminated metal "
            "may require special handling."
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

    st.subheader(f"♻️ {advice['name']} Detected")

    st.markdown(
        f"**Recommended Action:** {advice['action']}"
    )

    st.markdown(
        f"**Environmental Impact:** {advice['environment']}"
    )

    st.markdown(
        f"**Health Hazards:** {advice['health']}"
    )

    st.divider()

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
        )
    else:
        st.image(
            settings.DEFAULT_IMAGE,
            caption="Default Image",
            use_container_width=True
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
            )

            # Extract recognized waste categories
            detected_categories = set()

            if result.boxes is not None and len(result.boxes) > 0:

                for class_id in result.boxes.cls.tolist():
                    label = result.names[int(class_id)]
                    st.write("YOLO Detected Class:", label)

                    category = normalize_category(label)
                    st.write("Green Adviser Category:", category)

                    if category:
                        detected_categories.add(category)
                        st.success(
                    f"Detection completed: "
                    f"{len(result.boxes)} object(s) detected."
                )

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
