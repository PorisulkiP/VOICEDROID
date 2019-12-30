from hyperparams import Hyperparams as hp
import librosa

batch_size = hp.B  # размер батча берем из гиперпараметров

# Алфавит задается в файле с гиперпараметрами
vocab = "E абвгдеёжзийклмнопрстуфхцчшщъыьэюя-"

# Получаем сигнал фиксированной частоты дискретизации
y, sr = librosa.load(wavename, sr=hp.sr)

# Обрезаем тишину по краям
y, _ = librosa.effects.trim(y)

# Pre-emphasis фильтр
y = np.append(y[0], y[1:] - hp.preemphasis * y[:-1])

# Оконное преобразование Фурье
linear = librosa.stft(y=y,
                      n_fft=hp.n_fft,
                      hop_length=hp.hop_length,
                      win_length=hp.win_length)

# Амплитудный спектр
mag = np.abs(linear)

# Мел-спектр
mel_basis = librosa.filters.mel(hp.sr, hp.n_fft, hp.n_mels)
mel = np.dot(mel_basis, mag)

# Переводим в децибелы
mel = 20 * np.log10(np.maximum(1e-5, mel))
mag = 20 * np.log10(np.maximum(1e-5, mag))

# Нормализуем
mel = np.clip((mel - hp.ref_db + hp.max_db) / hp.max_db, 1e-8, 1)
mag = np.clip((mag - hp.ref_db + hp.max_db) / hp.max_db, 1e-8, 1)

# Транспонируем и приводим к нужным типам
mel = mel.T.astype(np.float32)
mag = mag.T.astype(np.float32)

# Добиваем нулями до правильных размерностей
t = mel.shape[0]
num_paddings = hp.r - (t % hp.r) if t % hp.r != 0 else 0
mel = np.pad(mel, [[0, num_paddings], [0, 0]], mode="constant")
mag = np.pad(mag, [[0, num_paddings], [0, 0]], mode="constant")

# Понижаем частоту дискретизации для мел-спектра
mel = mel[::hp.r, :]

def griffin_lim(spectrogram, n_iter=hp.n_iter):
    x_best = copy.deepcopy(spectrogram)
    for i in range(n_iter):
        x_t = librosa.istft(x_best,
                            hp.hop_length,
                            win_length=hp.win_length,
                            window="hann")
        est = librosa.stft(x_t,
                           hp.n_fft,
                           hp.hop_length,
                           win_length=hp.win_length)
        phase = est / np.maximum(1e-8, np.abs(est))
        x_best = spectrogram * phase
    x_t = librosa.istft(x_best,
                        hp.hop_length,
                        win_length=hp.win_length,
                        window="hann")
    y = np.real(x_t)
    return y









