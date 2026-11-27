# Ukur kemiripan wajah terhadap acuan: skor identitas ArcFace + rasio geometri wajah
import sys, cv2, numpy as np
from insightface.app import FaceAnalysis
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1, det_size=(640,640))
def face(p):
    img = cv2.imread(p); fs = app.get(img)
    if not fs: return None
    return max(fs, key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
def ratios(f):
    k = f.landmark_2d_106; d = lambda a,b: float(np.linalg.norm(k[a]-k[b]))
    fw = d(1,17)               # lebar wajah (pipi kiri-kanan, kontur)
    eyes = float(np.linalg.norm(f.kps[0]-f.kps[1]))   # jarak pusat mata
    nose_w = d(78,84) if k.shape[0]>84 else 0
    mouth_w = float(np.linalg.norm(f.kps[3]-f.kps[4]))
    eye_mid = (f.kps[0]+f.kps[1])/2
    chin = k[0]; face_h = float(np.linalg.norm(eye_mid-chin))
    nose_len = float(np.linalg.norm(eye_mid-f.kps[2]))
    return {'mata/lebar':eyes/fw,'mulut/mata':mouth_w/eyes,'hidung_pjg/mata':nose_len/eyes,'mata-dagu/mata':face_h/eyes,'pose(yaw,pitch,roll)':tuple(round(float(x),1) for x in f.pose)}
ref = face(sys.argv[1]); r0 = ratios(ref)
print('ACUAN', {k:(round(v,3) if isinstance(v,float) else v) for k,v in r0.items()})
for p in sys.argv[2:]:
    f = face(p)
    if f is None: print(p.split('/')[-1], 'WAJAH TIDAK TERDETEKSI'); continue
    sim = float(np.dot(ref.normed_embedding, f.normed_embedding)); r = ratios(f)
    dev = {k: f"{(r[k]/r0[k]-1)*100:+.1f}%" for k in r if isinstance(r[k],float)}
    print(f"{p.split('/')[-1]}: identitas={sim:.3f}  usia~{f.age} (acuan~{ref.age})  selisih rasio={dev}  pose={r['pose(yaw,pitch,roll)']}")
