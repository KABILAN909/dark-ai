# =========================================
# IMPORTS
# =========================================

from flask import Flask, render_template, request, jsonify
from groq import Groq
from tavily import TavilyClient

# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

# =========================================
# API KEYS
# =========================================

# LOCAL USE ONLY
# Replace with your real key while running locally

GROQ_API_KEY =""

TAVILY_API_KEY =""

# =========================================
# CLIENTS
# =========================================

client = Groq(
    api_key=GROQ_API_KEY
)

tavily = TavilyClient(
    api_key=TAVILY_API_KEY
)

# =========================================
# MEMORY
# =========================================

chat_history = []

# =========================================
# HOME
# =========================================

@app.route("/")
def home():
    return render_template("index.html")

# =========================================
# CHAT
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    # SAVE USER CHAT

    chat_history.append({
        "role": "user",
        "content": user_message
    })

    # =====================================
    # IMAGE GENERATION
    # =====================================

    if "create image" in user_message.lower():

        prompt = user_message.replace(
            "create image",
            ""
        )

        image_url = f"https://image.pollinations.ai/prompt/{prompt}"

        return jsonify({
            "reply": f"🎨 Image Generated\n\n{image_url}"
        })

    # =====================================
    # LIVE SEARCH
    # =====================================

    elif "latest" in user_message.lower() or \
         "news" in user_message.lower() or \
         "score" in user_message.lower() or \
         "weather" in user_message.lower():

        try:

            result = tavily.search(
                query=user_message,
                search_depth="basic",
                max_results=3
            )

            answer = ""

            for item in result["results"]:

                answer += (
                    f"🔹 {item['title']}\n"
                    f"{item['content']}\n\n"
                )

            return jsonify({
                "reply": answer
            })

        except Exception as e:

            return jsonify({
                "reply": f"❌ Search Error: {str(e)}"
            })

    # =====================================
    # AI CHAT
    # =====================================

    try:

        completion = client.chat.completions.create(

            model="llama3-70b-8192",

            messages=chat_history

        )

        reply = completion.choices[0].message.content

        # SAVE BOT REPLY

        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"❌ AI Error: {str(e)}"
        })

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)