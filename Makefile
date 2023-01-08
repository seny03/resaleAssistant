configurate_token:
	@read -p "Your TOKEN: " TOKEN && echo TOKEN="\"$${TOKEN}\"" >> ~/.bashrc
	@sudo source ~/.bashrc

install:
	python3 -m pip install -r requirements.txt

run3:
	@source ~/.bashrc
	@python3 markOutBot.py

run:
	@source ~/.bashrc
	@python markOutBot.py