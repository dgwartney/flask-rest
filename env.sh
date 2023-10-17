export FLASK_APP=rest
export FLASK_DEBUG=True
export FLASK_RUN_PORT=8000
export CONDA_ENV=flask-rest
export OPEN_WEATHER_API_KEY=

echo "Sourcing environment..."
conda env list | grep $CONDA_ENV
if  conda env list | grep $CONDA_ENV > /dev/null
then
  conda activate $CONDA_ENV
else
  echo "Python environment not configured"
fi

