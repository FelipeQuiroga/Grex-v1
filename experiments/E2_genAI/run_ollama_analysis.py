import csv
from collections import Counter, defaultdict
import ollama
from pathlib import Path



current_dir = Path(__file__).resolve().parent
e1_dir = current_dir.parent / "E1_cluster"
e1_output_csv = e1_dir / "output_bertopic_clusters.csv"

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

    print("📦 Carregando clusters já gerados no E1 (sem re-treinar)...")

    # Usamos o output consolidado do E1 para evitar re-treinar o BERTopic.
    # O CSV já contém o topic_id e termos principais por relato.
    if not e1_output_csv.exists():
        raise FileNotFoundError(f"❌ CSV do E1 não encontrado em {e1_output_csv}")

    clusters = defaultdict(list)
    topic_terms = defaultdict(list)
    topic_sectors = defaultdict(list)

    with e1_output_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            topic_id = int(row["topic_id"])
            texto = row["texto"].strip()
            setor = row.get("setor", "N/A").strip() or "N/A"
            terms = [t.strip() for t in row.get("top_terms", "").split(",") if t.strip()]

            clusters[topic_id].append(texto)
            topic_terms[topic_id].append(terms)
            topic_sectors[topic_id].append(setor)

    # 3. Loop de Interpretação com Ollama
    print(f"\n⚡ Iniciando inferência no {OLLAMA_MODEL}...")

    # Arquivo de saída na pasta E2
    output_file = Path("relatorio_ia_generativa.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Relatório de Interpretação Automática (Llama 3)\n\n")
        
        for topic_id in sorted(clusters.keys()):
            if topic_id == -1:
                continue  # Pula ruído

            exemplos = clusters[topic_id][:8]  # Limita a 8 exemplos

            # Consolida termos principais a partir do CSV do E1
            termos_flat = [t for terms in topic_terms[topic_id] for t in terms]
            termos = [t for t, _ in Counter(termos_flat).most_common(6)]

            setor_counts = Counter(topic_sectors[topic_id])
            setor = setor_counts.most_common(1)[0][0] if setor_counts else "N/A"
            stats = {'count': len(clusters[topic_id]), 'sector': setor}

            # Chama IA com dados já prontos do E1
            resultado = gerar_interpretacao_ollama(topic_id, termos, exemplos, stats)

            # Escreve no arquivo e na tela
            bloco = f"## Tópico {topic_id}\n{resultado}\n\n---\n"
            print(bloco)
            f.write(bloco)

    print(f"\n✅ Concluído! Relatório salvo em {output_file.resolve()}")

if __name__ == "__main__":
    main()
