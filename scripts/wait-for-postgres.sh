#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift

until PGPASSWORD=postgres psql -h "$host" -U postgres -d car_insurance -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"