# Adiciona e commita primeiro
git add scripts/
if ! git diff --cached --quiet; then
  git commit -m "FIX: Correction commit"
fi

# Depois atualiza a branch e faz push
git pull origin dev --rebase
git push origin dev
