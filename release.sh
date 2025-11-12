#!/bin/bash
# Script para fazer bump de patch e criar release automaticamente

set -e

echo "🚀 Iniciando processo de release..."

# Bump patch version
echo "📦 Fazendo bump de patch version..."
uv version --bump patch

# Pegar a nova versão
VERSION=$(uv version --short)
echo "✅ Nova versão: $VERSION"

# Adicionar arquivos
echo "📝 Adicionando arquivos ao git..."
git add pyproject.toml uv.lock

# Commit
echo "💾 Criando commit..."
git commit -m "chore: bump version to $VERSION"

# Criar tag
echo "🏷️  Criando tag v$VERSION..."
git tag -a "v$VERSION" -m "Release v$VERSION"

# Push
echo "🌐 Enviando para o GitHub..."
git push origin main --tags

echo ""
echo "✨ Release v$VERSION criada com sucesso!"
echo "🔗 Acompanhe o build em: https://github.com/felipeadeildo/pytally/actions"
