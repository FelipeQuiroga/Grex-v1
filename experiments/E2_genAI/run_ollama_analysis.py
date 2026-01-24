import sys
import pandas as pd
import ollama
from pathlib import Path



current_dir = Path(__file__).resolve().parent
e1_dir = current_dir.parent / "E1_cluster"
sys.path.append(str(e1_dir))

try:
    import run_bertopic_experiment as e1
except ImportError:
    print(f"❌ Erro: Não foi possível encontrar 'run_bertopic_experiment.py' em {e1_dir}")
    sys.exit(1)


from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN
from umap import UMAP

# ================= CONFIGURAÇÃO OLLAMA =================
OLLAMA_MODEL = "llama3:latest" 

def gerar_interpretacao_ollama(topic_id, termos, exemplos, stats):
    
    lista_exemplos = "\n".join([f"- {ex}" for ex in exemplos])
    
    prompt_sistema = """Você é um analista sênior de operações industriais. 
Sua tarefa é analisar grupos de problemas e criar resumos acionáveis para gestores.
Seja direto e técnico."""

    prompt_usuario = f"""
ANÁLISE DE CLUSTER (TÓPICO {topic_id})

DADOS:
- Total relatos: {stats['count']}
- Setor: {stats['sector']}
- Termos técnicos: {', '.join(termos)}

EXEMPLOS REAIS:
{lista_exemplos}

TAREFA:
Crie um resumo estruturado EXATAMENTE neste formato:
Label: [Nome curto, máx 5 palavras]
Resumo: [Explicação do problema e impacto, máx 2 frases]
Ação: [Uma ação prática sugerida]
"""

    print(f"   ↳ 🦙 Enviando Tópico {topic_id} para Llama 3...")
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {'role': 'system', 'content': prompt_sistema},
            {'role': 'user', 'content': prompt_usuario},
        ])
        return response['message']['content']
    except Exception as e:
        return f"Erro Ollama: {str(e)}"

def main():

    print("📦 Carregando dataset e stopwords do E1...")
    
    dataset_path = e1.DEFAULT_DATASET
    if not dataset_path.exists():
        dataset_path = e1_dir.parent / "E0_dataset_goldset" / "dataset.csv"
    
    df = e1.load_dataset(dataset_path)
    stopwords = e1.load_stopwords(e1.DEFAULT_STOPWORDS)
    
    texts = df["texto"].astype(str).str.strip().str.lower().tolist()
    
    print(f"🧠 Treinando BERTopic com modelo: {e1.EMBEDDING_MODEL_NAME}")
    
    e1.set_seed(e1.SEED_PRIMARY)
    
    hf_model = SentenceTransformer(e1.EMBEDDING_MODEL_NAME)
    
    # Configuração idêntica ao seu E1 (hardcoded aqui ou puxada se fossem variaveis)
    hdbscan_model = HDBSCAN(min_cluster_size=3, min_samples=1, cluster_selection_epsilon=0.5, metric='euclidean')
    umap_model = UMAP(n_neighbors=5, n_components=3, min_dist=0.0, metric='cosine')
    
    topic_model = BERTopic(
        embedding_model=hf_model,
        language=None,
        hdbscan_model=hdbscan_model,
        umap_model=umap_model,
        calculate_probabilities=False,
        verbose=True
    )
    
    topics, _ = topic_model.fit_transform(texts)
    df['topic'] = topics # Salva o tópico no dataframe para consulta

    # 3. Loop de Interpretação com Ollama
    print(f"\n⚡ Iniciando inferência no {OLLAMA_MODEL}...")
    
    info_topics = topic_model.get_topic_info()
    
    # Arquivo de saída na pasta E2
    output_file = Path("relatorio_ia_generativa.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Relatório de Interpretação Automática (Llama 3)\n\n")
        
        for index, row in info_topics.iterrows():
            topic_id = row['Topic']
            if topic_id == -1: continue # Pula ruído
                
            # Coleta dados
            termos = [t[0] for t in topic_model.get_topic(topic_id)[:6]]
            
            # Pega documentos representativos
            docs = topic_model.get_representative_docs(topic_id)
            # Se faltar representativos, completa com aleatórios
            if len(docs) < 5:
                extras = df[df['topic'] == topic_id]['texto'].head(5).tolist()
                docs = list(set(docs + extras))
            docs = docs[:8] # Limita a 8 exemplos
            
            setor = df[df['topic'] == topic_id]['setor'].mode()[0] if 'setor' in df.columns else "N/A"
            stats = {'count': row['Count'], 'sector': setor}
            
            # Chama IA
            resultado = gerar_interpretacao_ollama(topic_id, termos, docs, stats)
            
            # Escreve no arquivo e na tela
            bloco = f"## Tópico {topic_id}\n{resultado}\n\n---\n"
            print(bloco)
            f.write(bloco)

    print(f"\n✅ Concluído! Relatório salvo em {output_file.resolve()}")

if __name__ == "__main__":
    main()