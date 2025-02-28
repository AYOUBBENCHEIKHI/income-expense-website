import smtplib

"""EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_PORT = 2525
EMAIL_HOST_USER = "008b042df4b8ac"
EMAIL_HOST_PASSWORD = "d53fd6b6d231d4"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"""

EMAIL_HOST = 'smtp.gmail.com'  # Change si tu utilises un autre fournisseur
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ayoubbencheikhi03@gmail.com'
EMAIL_HOST_PASSWORD = 'lmek eigh barl umua'

try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("Connexion SMTP réussie ! ✅")
    server.quit()
except Exception as e:
    print(f"Erreur SMTP ❌: {e}")
