cd ./frontend
npm install
if [ $? -ne 0 ]; then
    echo "Failed to restore frontend npm packages"
    exit $?
fi

echo ""
echo "Building frontend"
echo ""

npm run build
if [ $? -ne 0 ]; then
    echo "Failed to build frontend"
    exit $?
fi
