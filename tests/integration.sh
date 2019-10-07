event() {
  status=$1
  mirror=$2
  commit=$3

  echo {} | \
  jq -r \
  --arg status $status \
  --arg mirror $mirror \
  --arg commit $commit \
  --arg log_url "https://console.cloud.google.com/gcr/builds/aeccd2ef-f51a-4a44-8e2e-0de2609ce367?project=292927648743" \
  --arg build_trigger_id "2bceb582-3141-44bf-b444-5640cbcaecc5" \
  '.status = $status | .sourceProvenance.resolvedRepoSource.repoName = $mirror | .sourceProvenance.resolvedRepoSource.commitSha = $commit | .logUrl = $log_url | .buildTriggerId = $build_trigger_id | @base64 | {"data": . }'
}

run_test() {
  build_status=$1
  provider_status=$2
  provider=$3
  owner=$4
  repo=$5
  commit=$6
  username=$7
  password=$8
  url=$9
  mirror=${provider}_${owner}_${repo}

  gcloud functions call cloud-build-status --data "$(event $build_status $mirror $commit)"

  curl -sS -u $username:$password \
    https://api.bitbucket.org/2.0/repositories/${owner}/${repo}/commit/${commit}/statuses | \
    jq -e --arg status $provider_status '.values[0].state == $status'
}

run_github_test() {
  run_test $1 $2 "github" $GITHUB_REPO_OWNER $GITHUB_REPO $GITHUB_COMMIT_SHA \
    $GITHUB_USERNAME \
    $GITHUB_PASSWORD \
    https://api.github.com/repos/${GITHUB_REPO_OWNER}/${GITHUB_REPO}/statuses/${GITHUB_COMMIT_SHA}
}

run_bitbucket_test() {
  run_test $1 $2 "bitbucket" $BB_REPO_OWNER $BB_REPO $BB_COMMIT_SHA \
    $BB_USERNAME \
    $BB_PASSWORD \
    https://api.bitbucket.org/2.0/repositories/${BB_REPO_OWNER}/${BB_REPO}/commit/${BB_COMMIT_SHA}/statuses
}
