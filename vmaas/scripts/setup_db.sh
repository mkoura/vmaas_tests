#!/usr/bin/env bash

USAGE="Usage:
$0 REPOLIST_PATH TARGET_HOSTNAME [PROJECT_PATH]

Mandatory parameters:
  REPOLIST_PATH   - Path to the repolist.json file
  TARGET_HOSTNAME - Hostname of the target machine where vmaas server is running

Optional parameters:
  PROJECT_PATH - Path to the project to speed up waiting for tasks; only works
                 when TARGET_HOSTNAME is 'localhost' and both the client and server
                 are running in the same timezone (VMaaS server runs in UTC by default)
"

tse_before=$(date +%s)

# wait_task <message_in_log> <timeout_in_sec> <project_path>
wait_task() {
  cd "$3"
  tmpl_last="docker-compose logs | grep \"<message>\" | tail -n 1 | egrep -o \"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})\"| xargs --no-run-if-empty -0 date +%s -d"
  last=${tmpl_last//<message>/$1}
  while true; do
    tse_last="$(eval $last)"
    if [ -n "$tse_last" ] && [ "$tse_last" -ge "$tse_before" ]; then
      break
    elif [ $(expr "$(date +%s)" - "$tse_before") -gt $2 ]; then
      break
    fi
    sleep 2
done
}

# sleep_or_wait <message_in_log> <timeout_in_sec> <project_path>
sleep_or_wait() {
  if [ -z "$3" ]; then
    sleep "$2"
  else
    wait_task "$1" "$2" "$3"
  fi
}

# 2 arguments expected, 3 if TARGET_HOSTNAME is localhost / 127.0.0.1
if ! ([ "$#" -eq "2" ] || ([ "$#" -eq "3" ] && ([ "$2" == "localhost" ] || [ "$2" == "127.0.0.1" ]))); then
	printf "$USAGE"
	exit 1
fi

printf "Step 1/2: Repo sync\nAPI Response: "
curl -d "@$1" -X POST "http://$2:8081/api/v1/sync/repo"
printf "\n"
sleep_or_wait "Repo sync task finished: OK" 300 $3

printf "Step 2/2: CVE sync\nAPI Response: "
curl -X GET "http://$2:8081/api/v1/sync/cve"
printf "\n"
sleep_or_wait "CVE sync task finished: OK" 120 $3

printf "WORKAROUND GH#271: "
curl -X GET "http://$2:8081/api/v1/sync/export"
printf "\n"
sleep_or_wait "WORKAROUND export task finished: OK" 120 $3

printf "Done.\n"
