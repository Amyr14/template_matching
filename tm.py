import cv2 as cv
import ffmpeg
import pandas
import json
import os
import shutil
import tempfile

inputs_dir = os.path.join(os.getcwd(), 'inputs')
config_file = open("input_config.json")
config = json.load(config_file)

input_path = os.path.join(inputs_dir, config['video'])
template_path = os.path.join(inputs_dir, config['template'])

src_video = cv.VideoCapture(input_path)

# Extraindo metadados do vídeo
video_w = int(src_video.get(cv.CAP_PROP_FRAME_WIDTH))
video_h = int(src_video.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = src_video.get(cv.CAP_PROP_FPS)


# Criando o diretório temporário
temp_dir = tempfile.mkdtemp(dir=os.getcwd())

# Padrão de nomes de frames
frame_pattern = os.path.join(temp_dir, 'frame-%d.png')

(
    ffmpeg.input(input_path)
    .output(frame_pattern, vf=f'fps={fps}')
    .run()
)


# Abrindo o template e recuperando suas dimensões
template = cv.imread(template_path, cv.IMREAD_GRAYSCALE).copy()
template_h, template_w = template.shape


# Os métodos de template matching a serem testados
tm_methods = [
    'cv.TM_CCOEFF', 
    'cv.TM_CCOEFF_NORMED',
    'cv.TM_CCORR',
    'cv.TM_CCORR_NORMED',
    'cv.TM_SQDIFF',
    'cv.TM_SQDIFF_NORMED'
]

dfs = []

for method in tm_methods:
    min_vals = []
    max_vals = []
    min_locs = []
    max_locs = []
    method = eval(method)

    for frame in os.listdir(temp_dir):
        # Lendo frame
        frame = os.path.join(temp_dir, frame)
        frame_img = cv.imread(frame, cv.IMREAD_GRAYSCALE).copy()
        
        # Executando o template matching
        result = cv.matchTemplate(frame_img, template, method)

        # Recuperando e registrando valores mínimos, máximos e sus coordenadas
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        min_vals.append(min_val)
        max_vals.append(max_val)
        max_locs.append(max_loc)
        min_locs.append(min_loc)

    data = {
        'min_val': min_vals,
        'max_val': max_vals,
        'min_loc': min_locs,
        'max_loc': max_locs,
    }

    dfs.append(pandas.DataFrame(data))


columns_to_plot = ['min_val', 'max_val']

for method, df in zip(tm_methods, dfs):
    df[columns_to_plot].plot(
        figsize=(16,8),
        title=method,
        xlabel='Frame',
        ylabel='Valor',
    )


output_path = os.path.join(os.getcwd(), 'outputs', 'tracking.mp4')

codec = cv.VideoWriter_fourcc(*'mp4v')

# Objeto VideoWriter, usado para escrever os frames
out_video = cv.VideoWriter(
    output_path,
    codec,
    fps,
    (video_w, video_h),
    isColor=False
)

# Recuperando os valores máximos e suas coordenadas
max_vals = dfs[1]['max_val']
max_locs = dfs[1]['max_loc']

# Definindo threshold
tresh = 0.45

# Iterando sobre os frames, transformando-os e escrevendo-os um por um
for idx, frame in enumerate(os.listdir(temp_dir)):

    # Lendo frame
    frame = os.path.join(temp_dir, frame)
    frame_img = cv.imread(frame, cv.IMREAD_GRAYSCALE)
    
    # Desenhando um retangulo para evidenciar o objeto
    max_val = max_vals[idx]
    max_loc = max_locs[idx]

    # Escrever o frame sem transformacao
    if max_val < tresh:
        out_video.write(frame_img)

    else:
        top_left = max_loc
        bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
        cv.rectangle(frame_img, top_left, bottom_right, 255, 2)
        out_video.write(frame_img)

# Fechando todos os buffers
src_video.release()
out_video.release()
cv.destroyAllWindows()

# Removendo diretório temporário
shutil.rmtree(temp_dir)


