<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NOFA CONTENT FACTORY - LIVE ENGINE</title>
    <style>
        /* UI/UX PRESET: BLUE-GREY PREMIUM */
        body { background-color: #f0f2f5; color: #1c1e21; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 95%; max-width: 420px; background: #ffffff; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0, 123, 255, 0.15); text-align: center; border: 1px solid #dcdfe3; }
        .header h1 { color: #007bff; margin: 0; font-size: 1.6rem; letter-spacing: 1px; }
        .status-row { display: flex; justify-content: space-between; margin: 15px 0; font-size: 0.8rem; font-weight: bold; }
        .progress-box { text-align: left; margin-bottom: 10px; }
        .progress-label { display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 4px; color: #606770; }
        .bar-bg { width: 100%; height: 8px; background: #e4e6eb; border-radius: 10px; overflow: hidden; }
        .bar-fill { height: 100%; background: #007bff; transition: 0.5s; width: 0%; }
        .stat-card { background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 15px 0; border: 1px solid #007bff; position: relative; }
        #displayBalance { margin: 8px 0 0; font-size: 2.2rem; font-weight: 800; color: #007bff; }
        #levelTag { position: absolute; top: -10px; right: 10px; background: #007bff; color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.7rem; }
        .btn-group { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
        button { padding: 14px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .btn-wd { background: #007bff; color: white; }
        #log-transaksi { background: #ffffff; margin-top: 20px; height: 120px; border-radius: 12px; padding: 12px; font-family: 'Consolas', monospace; font-size: 0.75rem; overflow-y: auto; text-align: left; border: 1px solid #ced4da; }
        .log-entry { color: #0056b3; margin: 4px 0; border-bottom: 1px solid #f0f2f5; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>NOFA FACTORY</h1>
        <div class="status-row">
            <span>DATABASE: <span id="dbStatus" style="color: orange;">CONNECTING...</span></span>
            <span id="multiplierShow">BOOSTER: 1.0x</span>
        </div>
    </div>

    <div class="progress-box">
        <div class="progress-label"><span>XP PROGRESS</span><span id="xpText">0/100</span></div>
        <div class="bar-bg"><div id="xpBar" class="bar-fill"></div></div>
    </div>

    <div class="stat-card">
        <div id="levelTag">LVL 1</div>
        <h2>TOTAL REVENUE</h2>
        <p id="displayBalance">Rp 0</p>
    </div>

    <div class="btn-group">
        <button class="btn-wd" onclick="tarikSaldo()">WITHDRAW PROFITS</button>
    </div>

    <div id="log-transaksi"><p class="log-entry">Booting Engine...</p></div>
</div>

<script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
    import { getDatabase, ref, onValue, update, increment } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";

    // CONFIG ASLI DARI CHIEF
    const firebaseConfig = {
        apiKey: "AIzaSyCk9wfztKVcLJ2ved90wKEBgCsQ5qA11Yg", // Pastikan ganti koma dengan key asli lo
        authDomain: "nofa-content-factory.firebaseapp.com",
        projectId: "nofa-content-factory",
        storageBucket: "nofa-content-factory.firebasestorage.app",
        messagingSenderId: "997810554232",
        appId: "1:997810554232:web:7d9c70cd6bc6501075748d",
        databaseURL: "https://nofa-content-factory-default-rtdb.asia-southeast1.firebasedatabase.app/" // Sesuaikan URL DB lo
    };

    const app = initializeApp(firebaseConfig);
    const db = getDatabase(app);
    const USER_ID = "CHIEF_ADMIN"; // ID Identitas di Database

    function tambahLog(pesan) {
        const logContainer = document.getElementById('log-transaksi');
        const entri = document.createElement('p');
        entri.className = "log-entry";
        entri.innerHTML = `[${new Date().toLocaleTimeString()}] ${pesan}`;
        logContainer.prepend(entri);
    }

    // LISTENER DATA DARI SERVER (UI SINKRON)
    const userRef = ref(db, 'users/' + USER_ID);
    onValue(userRef, (snapshot) => {
        const data = snapshot.val();
        if (data) {
            document.getElementById('displayBalance').innerText = "Rp " + Math.floor(data.balance).toLocaleString('id-ID');
            document.getElementById('levelTag').innerText = "LVL " + data.level;
            document.getElementById('xpBar').style.width = (data.xp % 100) + "%";
            document.getElementById('xpText').innerText = (data.xp % 100) + "/100";
            document.getElementById('dbStatus').innerText = "ONLINE";
            document.getElementById('dbStatus').style.color = "#28a745";
        } else {
            // Inisialisasi User Baru di Firebase
            update(userRef, { balance: 0, level: 1, xp: 0 });
        }
    });

    // MINING ENGINE (AUTO-UPDATE KE SERVER)
    setInterval(() => {
        update(userRef, {
            balance: increment(Math.floor(Math.random() * 500) + 100),
            xp: increment(5)
        }).then(() => {
            tambahLog("Server Synced: Profit +XP Collected.");
        }).catch(err => {
            tambahLog("Error: " + err.message);
        });
    }, 5000); // Jalan tiap 5 detik ke Database

    window.tarikSaldo = () => {
        alert("Fungsi WD sedang memverifikasi Ledger Server...");
        tambahLog("WD Request sent to server.");
    };
</script>

</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NOFA - AI Image Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            color: #2c3e50;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        textarea, select {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }
        button {
            padding: 12px 25px;
            background-color: #3498db; /* Warna biru */
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        #statusMessage {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            background-color: #e7f3fe; /* Latar belakang biru muda */
            color: #3498db;
            border: 1px solid #bce8f1;
            display: none; /* Sembunyikan secara default */
        }
        #statusMessage.error {
            background-color: #f2dede; /* Latar belakang merah muda */
            color: #a94442;
            border: 1px solid #ebccd1;
        }
        #statusMessage.success {
            background-color: #dff0d8; /* Latar belakang hijau muda */
            color: #3c763d;
            border: 1px solid #d6e9c6;
        }
        #imageOutput {
            margin-top: 30px;
            text-align: center;
        }
        #imageOutput img {
            max-width: 100%;
            height: auto;
            border: 1px solid #eee;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>NOFA Content Factory</h1>
        <p>Gunakan AI untuk menghasilkan gambar sesuai kebutuhan konten Anda.</p>

        <div class="image-generator-section">
            <h2>AI Image Generator</h2>
            <div>
                <label for="imagePrompt">Deskripsi Gambar (Prompt):</label>
                <textarea id="imagePrompt" rows="5" placeholder="Contoh: Pemandangan kota futuristik saat matahari terbenam, dengan mobil terbang, gaya cyberpunk, detail tinggi"></textarea>
            </div>
            <div>
                <label for="aspectRatio">Rasio Aspek:</label>
                <select id="aspectRatio">
                    <option value="">Pilih Rasio Aspek (Default: Square)</option>
                    <option value="1:1">1:1 (Contoh: Instagram Post, Profil)</option>
                    <option value="16:9">16:9 (Contoh: YouTube Thumbnail, Header Website)</option>
                    <option value="9:16">9:16 (Contoh: Instagram Story, TikTok, Potret)</option>
                </select>
            </div>
            <button id="generateImageBtn">Generate Gambar</button>

            <div id="statusMessage"></div>
            <div id="imageOutput">
                <!-- Gambar yang dihasilkan akan muncul di sini -->
            </div>
        </div>
    </div>

    <script>
        // --- PENTING: GANTI DENGAN URL FIREBASE FUNCTION generateImage ANDA ---
        const GENERATE_IMAGE_FUNCTION_URL = "https://<REGION>-<PROJECT_ID>.cloudfunctions.net/generateImage";
        // Contoh: "https://asia-southeast1-nofa-content-factory.cloudfunctions.net/generateImage";

        document.addEventListener('DOMContentLoaded', () => {
            const imagePromptInput = document.getElementById('imagePrompt');
            const aspectRatioSelect = document.getElementById('aspectRatio');
            const generateImageBtn = document.getElementById('generateImageBtn');
            const statusMessageDiv = document.getElementById('statusMessage');
            const imageOutputDiv = document.getElementById('imageOutput');

            generateImageBtn.addEventListener('click', async () => {
                const prompt = imagePromptInput.value.trim();
                const aspectRatio = aspectRatioSelect.value; // Ambil nilai rasio aspek yang dipilih

                if (!prompt) {
                    displayStatus('Harap masukkan deskripsi gambar!', 'error');
                    return;
                }

                displayStatus('Sedang membuat gambar, mohon tunggu...', 'info');
                generateImageBtn.disabled = true; // Nonaktifkan tombol selama proses

                imageOutputDiv.innerHTML = ''; // Kosongkan output sebelumnya

                try {
                    const response = await fetch(GENERATE_IMAGE_FUNCTION_URL, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ prompt: prompt, aspectRatio: aspectRatio }), // Kirim prompt dan aspectRatio
                    });

                    if (!response.ok) {
                        const errorData = await response.text(); // Ambil teks error dari server
                        throw new Error(`Server error (${response.status}): ${errorData}`);
                    }

                    const data = await response.json();

                    if (data.imageUrl) {
                        const imgElement = document.createElement('img');
                        imgElement.src = data.imageUrl;
                        imgElement.alt = "Generated Image";
                        imageOutputDiv.appendChild(imgElement);

                        displayStatus('Gambar berhasil dibuat!', 'success');
                    } else {
                        throw new Error('Tidak ada imageUrl dalam respons dari AI.');
                    }

                } catch (error) {
                    console.error('Error generating image:', error);
                    displayStatus(`Gagal membuat gambar: ${error.message}`, 'error');
                } finally {
                    generateImageBtn.disabled = false; // Aktifkan kembali tombol
                }
            });

            // Fungsi pembantu untuk menampilkan pesan status
            function displayStatus(message, type) {
                statusMessageDiv.textContent = message;
                statusMessageDiv.className = ''; // Reset class
                statusMessageDiv.style.display = 'block'; // Tampilkan div
                if (type === 'error') {
                    statusMessageDiv.classList.add('error');
                } else if (type === 'success') {
                    statusMessageDiv.classList.add('success');
                } else { // info
                    statusMessageDiv.classList.add('info');
                }
            }
        });
    </script>
</body>
</html>
