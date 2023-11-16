import git

from git.repo import Repo
import os

download_path = os.path.join('test', 't1')
Repo.clone_from('https://gitee.com/xzyxw10592191MrChen/Tidy_Terminal.git', to_path=os.path.join('Tidy-terminal'), branch='master')