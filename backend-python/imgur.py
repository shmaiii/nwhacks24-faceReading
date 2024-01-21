import pyimgur

def upload_imgur():
    client_id = 'ee52a5df0524c14'
    headers = {'Authorization': 'Client-ID' + client_id}
    im = pyimgur.Imgur(client_id)
    uploaded_image = im.upload_image("face_mesh/annotated_image.jpg", title="Annotated Imgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.size)
    print(uploaded_image.type)

    return uploaded_image.link

if __name__ == "__main__":
    upload_imgur()