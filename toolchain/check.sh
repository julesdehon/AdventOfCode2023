_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_ROOT_DIR="$(readlink -f "$_SCRIPT_DIR/../")"
source "$_ROOT_DIR/toolchain/colours.sh"

if ! black --preview --check "$_ROOT_DIR"; then
  echo "${RED}[RESULT:ERROR] Code is NOT formatted correctly; run: format.sh${NO_COLOR}"
  exit 1
fi

if ! isort "$_ROOT_DIR" --check; then
  echo "${RED}[RESULT:ERROR] Imports are NOT sorted correctly; run: make format.sh${NO_COLOR}"
  exit 1
fi

echo "Running flake8"
OUTPUT="$(flake8 "$_ROOT_DIR" 2>&1)"
EXIT_CODE=$?
if [ $EXIT_CODE != 0 ]; then
    echo "${OUTPUT//$_ROOT_DIR\//}"
    echo "${RED}[RESULT:ERROR] flake8 found files with errors: fix these errors manually${NO_COLOR}"
    exit 1
fi
echo "${GREEN}flake8 did not find any errors${NO_COLOR}"

echo "Running pylint"
if ! pylint $(git ls-files "$_ROOT_DIR/*.py") ; then
    echo "${RED}[RESULT:ERROR] pylint found files with errors: fix these errors manually${NO_COLOR}"
    exit 1
fi
echo "${GREEN}pylint did not find any errors${NO_COLOR}"

echo "Running static analysis"
if ! mypy --disallow-untyped-defs --disallow-untyped-calls $_ROOT_DIR; then
    echo "${RED}[RESULT:ERROR] mypy found issues: fix these errors manually;${NO_COLOR}"
    exit 1
fi
echo "${GREEN}static analysis did not find any errors${NO_COLOR}"

echo "${GREEN}[RESULT:SUCCESS] No linter issues found.${NO_COLOR}"