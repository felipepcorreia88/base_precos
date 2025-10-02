# 📦 Backup de Arquivos Antigos

Esta pasta contém arquivos e scripts antigos que não são necessários para o sistema principal de processamento parte por parte.

## 📂 Conteúdo

### Scripts Alternativos (não recomendados)
- **processar_completo.py** - Processa tudo de uma vez (3-4 horas sem pausa)
- **testar_modo_inteligente.py** - Teste antigo com servidor Flask
- **visualizador_materiais.py** - Visualizador com servidor Flask
- **visualizar_exemplo.sh** - Script para rodar visualizador Flask

### Documentação Redundante
- **README_FLUXO.md** - Documentação duplicada (já está em FLUXO_RECOMENDADO.md)

### Pastas Antigas
- **backup_original/** - Módulos de busca antigos (Mercado Livre, BuscaPé, Zoom)
- **testes_antigos/** - Scripts de teste anteriores
- **docs/** - Documentação antiga (substituída pelos MDs na raiz)

## ℹ️ Por que foram movidos?

Estes arquivos foram movidos para simplificar o diretório principal e focar no **fluxo recomendado**:
- Processar uma parte de cada vez
- Validar manualmente
- Exportar Excel

## 🔄 Como restaurar

Se precisar de algum arquivo antigo:

```bash
# Ver conteúdo do backup
ls -la backup_antigo/

# Copiar arquivo específico de volta
cp backup_antigo/processar_completo.py .
```

## ⚠️ Importante

Estes arquivos **NÃO são necessários** para o funcionamento do sistema atual. Foram mantidos apenas como backup histórico.

---

**Data do backup:** $(date '+%Y-%m-%d %H:%M:%S')

