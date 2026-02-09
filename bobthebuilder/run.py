from app.services.Crm import app
import os

# [핵심] Flask에게 templates 폴더가 어디 있는지 명확하게 알려줍니다.
app.template_folder = os.path.abspath("templates")
app.static_folder = os.path.abspath("static")

if __name__ == '__main__':
    # 여기서 전원을 켭니다!
    app.run(host='0.0.0.0', port=5000, debug=True)