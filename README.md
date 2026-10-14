# ⚛️ Q-Tac-Toe: Bridging Quantum Mechanics and Gaming
### (क्वांटम मैकेनिक्स और गेमिंग का अनूठा संगम)

A modern, interactive, and mathematically rigorous implementation of **Quantum Tic-Tac-Toe** built with Python and Pygame for hackathons and educational STEM exhibitions.

---

## 🏆 हाकाथॉन प्रोजेक्ट रिपोर्ट (Hackathon Project Report)

### 1. प्रोजेक्ट का नाम (Project Title)
**Q-Tac-Toe: Bridging Quantum Mechanics and Gaming**  
*(क्वांटम मैकेनिक्स और गेमिंग का अनूठा संगम)*

### 2. सार / कार्यकारी सारांश (Executive Summary)
पारंपरिक टिक-टैक-टो (Classical Tic-Tac-Toe) गेम हमेशा 'ड्रॉ' (Draw) पर समाप्त होता है। इस प्रोजेक्ट का उद्देश्य क्वांटम भौतिकी के जटिल सिद्धांतों—जैसे **Superposition** (सुपरपोजिशन), **Entanglement** (एंटैंगलमेंट), और **Wavefunction Collapse** (कोलैप्स)—को एक इंटरैक्टिव और मजेदार बोर्ड गेम के माध्यम से आम लोगों और छात्रों के लिए सरल बनाना है।

### 3. समस्या कथन (Problem Statement)
क्वांटम कंप्यूटिंग और क्वांटम मैकेनिक्स के सिद्धांत अमूर्त (Abstract) और कठिन होते हैं क्योंकि वे वास्तविक जीवन में सीधे दिखाई नहीं देते। इससे शुरुआती लोगों के लिए इन्हें समझना कठिन हो जाता है।

### 4. हमारा समाधान (Proposed Solution)
हमने क्लासिकल टिक-टैक-टो के नियमों में क्वांटम मैकेनिक्स के मूलभूत नियमों को लागू किया है:
1. **Superposition (सुपरपोजिशन)**: खिलाड़ी अपनी एक ही चाल ($X_k$ या $O_k$) को एक साथ दो अलग-अलग खानों (Boxes) में चलता है (यानी मार्क दोनों जगहों पर 50% संभावना $|\psi\rangle = \frac{1}{\sqrt{2}}(|A\rangle + |B\rangle)$ के साथ मौजूद रहता है)।
2. **Entanglement (एंटैंगलमेंट)**: जैसे-जैसे खिलाड़ी चालें चलते हैं, डिब्बों में एक-दूसरे के मार्क्स ओवरलैप होने लगते हैं, जिससे एक क्वांटम मल्टी-ग्राफ (Multigraph) का निर्माण होता है।
3. **Wavefunction Collapse (वेवफंक्शन कोलैप्स)**: जैसे ही बोर्ड पर चालों का कोई बंद चक्र (Cyclic Loop) बनता है, क्वांटम अनिश्चितता खत्म हो जाती है और विरोधी खिलाड़ी (Opponent) को यह तय करने का मौका मिलता है कि चक्र किस डिब्बे में टूटेगा, जिससे चालें पक्की (Classical) हो जाती हैं।
4. **Allan Goff's Quantum Tie-Breaker**: यदि एक ही कोलैप्स में दोनों खिलाड़ी 3-इन-ए-रो बनाते हैं, तो जिस खिलाड़ी की जीत का अधिकतम सबस्क्रिप्ट छोटा होता है, वह जीतता है।

---

## 🚀 मुख्य विशेषताएँ (Key Features Implemented)

- 🤖 **Single-Player vs Quantum AI**:
  - MiniMax और Probabilistic Decision Making पर आधारित स्मार्ट AI बॉट।
  - AI संभावित लूप्स, विनिंग लाइन्स और कोलैप्स ब्रांचेस का विश्लेषण करके सर्वोत्तम चाल चलता है।
  - कठिनाई स्तर: **Normal** और **Master** (Hard)।
- 🔊 **Procedural Sci-Fi Audio System**:
  - `NumPy` और `Pygame Mixer` के ज़रिए बिना किसी बाहरी `.wav` फ़ाइल के शुद्ध गणितीय सिंथेसाइज़र (Sine/Sawtooth + Envelope Decay) द्वारा साउंड इफेक्ट्स तैयार किए गए हैं।
  - Move Placement, Cycle/Loop Warning, Wavefunction Collapse, और Victory Chords शामिल हैं।
  - ऑडियो म्यूट/अनम्यूट टॉगल उपलब्ध।
- 🎨 **Catppuccin Neon UI & Starfield**:
  - Catppuccin Mocha कलर पैलेट (`#1e1e2e`, Cyan `#89dceb`, Mauve `#cba6f7`, Alert Red `#f38ba8`)।
  - मल्टी-लेयर अल्फा-ब्लेंडिंग नियॉन ग्लो इफेक्ट्स।
  - बैकग्राउंड में तैरते हुए क्वांटम पार्टिकल्स (Starfield)।
  - इंटैंगलमेंट थ्रेड्स (Glowing Quantum Connections)।
- 📖 **Interactive Tutorial Overlay**:
  - 4 विस्तृत स्लाइड्स जो सुपरपोजिशन, एंटैंगलमेंट, वेवफंक्शन कोलैप्स और स्कोरिंग को इंटरैक्टिव रूप से समझाती हैं।
  - किसी भी समय `📖 Guide (?)` बटन या `T` / `?` दबाकर खोला जा सकता है।
- ⚡ **Real-time Quantum Diagnostics**:
  - स्क्रीन पर हर चाल के साथ वास्तविक समय में भौतिकी के नियम और स्टेट वेक्टर $|\psi\rangle$ दिखाई देते हैं।

---

## 🛠️ तकनीक और टूल्स (Tech Stack)

| घटक (Component) | तकनीक (Technology) |
|---|---|
| **Programming Language** | Python 3.12+ |
| **Graphics & Game Loop** | Pygame 2.6+ |
| **Data Structures** | Graphs (Adjacency List, BFS Cycle Detection, Cascading Queue) |
| **Audio Synthesis** | NumPy (16-bit PCM waveform generation) & Pygame Mixer |
| **AI Algorithm** | Modified Minimax with Collapse Branch Simulation |
| **Theme / Design** | Catppuccin Mocha Neon Palette |

---

## 🎮 गेम कैसे चलाएं (How to Run)

### 1. लाइब्रेरीज़ इंस्टॉल करें
```bash
pip install -r requirements.txt
```

### 2. गेम शुरू करें
```bash
python main.py
```

### 3. कीबोर्ड शॉर्टकट्स (Controls)
- `R`: नया गेम रीसेट करें (Reset Game)
- `M`: साउंड म्यूट / अनम्यूट करें (Toggle Mute)
- `T` या `?`: ट्यूटोरियल खोलें (Open Tutorial)
- `A`: AI मोड और 2-प्लेयर मोड में स्विच करें (Toggle AI)
- `Esc`: ट्यूटोरियल बंद करें या चयन रद्द करें (Deselect)

---

## 📁 प्रोजेक्ट संरचना (Project Structure)

```
d:\QTTT\
│
├── main.py             # मुख्य Pygame लूप, GUI, इवेंट हैंडलिंग और नियॉन रेंडरिंग
├── quantum_board.py    # क्वांटम बोर्ड इंजन, साइकिल डिटेक्शन और कैस्केड कोलैप्स लॉजिक
├── quantum_ai.py       # AI बॉट (मिनीमैक्स, स्कोरिंग और प्रोबेबिलिस्टिक डिसीजन)
├── sound_effects.py    # NumPy आधारित 16-bit PCM प्रोसीजरल साउंड सिंथेसाइज़र
├── ui_theme.py         # Catppuccin Mocha पैलेट, नियॉन ग्लो और पार्टिकल सिस्टम
├── tutorial.py         # इंटरैक्टिव ट्यूटोरियल ओवरले (4 विस्तृत गाइड्स)
├── requirements.txt    # प्रोजेक्ट डिपेंडेंसीज़ (pygame, numpy)
└── README.md           # विस्तृत हाकाथॉन प्रोजेक्ट रिपोर्ट और दस्तावेज़
```
