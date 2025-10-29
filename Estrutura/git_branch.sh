# Configura o Git para usar SSH em vez de HTTPS 
git remote set-url origin git@github.com:Ronynetwork/PAPEMLS.git
git config user.name "Jenkins"
git config user.email "jenkins@correction"

# Muda para a branch dev
git branch dev
git checkout dev

# Restaura todos os arquivos exceto os da pasta scripts/
git restore --source=HEAD --staged --worktree -- :!scripts/

# Adiciona e commita primeiro
git add scripts/
if ! git diff --cached --quiet; then
  git commit -m "FIX: Correction commit"
fi

# Depois atualiza a branch e faz push
git push origin dev
git pull origin dev --rebase
