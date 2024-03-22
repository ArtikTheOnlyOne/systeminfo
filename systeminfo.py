import tkinter, subprocess

MODULE_WIDTH = 480
MODULE_HEIGHT = 320
OUTSET = 8
BORDER = 4

WIDTH = 464
HEIGHT = 40

def module(window, name, orientation, x, y):
    module = tkinter.Canvas(window, width=480, height=320, background="black", highlightthickness=0)
    module.pack()
    module.place(x=x, y=y)
    
    if orientation:
        temperature_x1 = OUTSET
        temperature_y1 = MODULE_HEIGHT - OUTSET - HEIGHT

        temperature_x2 = MODULE_WIDTH - OUTSET
        temperature_y2 = MODULE_HEIGHT - OUTSET

        load_x1 = OUTSET
        load_y1 = OUTSET

        load_x2 = MODULE_WIDTH - OUTSET
        load_y2 = OUTSET + WIDTH

        load_text_y = load_y1 + HEIGHT / 2 + 4

        extent = -180
    else:
        temperature_x1 = OUTSET
        temperature_y1 = OUTSET

        temperature_x2 = MODULE_WIDTH - OUTSET
        temperature_y2 = OUTSET + HEIGHT

        load_x1 = OUTSET
        load_y1 = MODULE_HEIGHT - OUTSET - WIDTH

        load_x2 = MODULE_WIDTH - OUTSET
        load_y2 = MODULE_HEIGHT - OUTSET

        load_text_y = load_y2 - HEIGHT / 2 - 4

        extent = 180

    temperature = module.create_rectangle(temperature_x1, temperature_y1, temperature_x2, temperature_y2, fill="green")

    module.create_rectangle(temperature_x1, temperature_y1, temperature_x2, temperature_y2, outline="white", width=4)

    temperature_text = module.create_text(MODULE_WIDTH / 2, temperature_y1 + HEIGHT / 2, text="0°C", fill="black", font=("Squares Bold", 24))
    
    load = module.create_arc(load_x1, load_y1, load_x2, load_y2)
    module.itemconfigure(load, fill="green")
    module.itemconfigure(load, start=180, extent=extent)

    border = module.create_arc(load_x1, load_y1, load_x2, load_y2)
    module.itemconfigure(border, outline="white", width=4)
    module.itemconfigure(border, start=180, extent=extent)
    
    background = module.create_arc(load_x1 + HEIGHT + OUTSET / 2, load_y1 + HEIGHT + OUTSET / 2, load_x2 - HEIGHT - OUTSET / 2, load_y2 - HEIGHT - OUTSET / 2)
    module.itemconfigure(background, fill="black", outline="white", width=4)
    module.itemconfigure(background, start=180, extent=extent)

    load_text = module.create_text(MODULE_WIDTH / 2, load_text_y, text="0%", fill="white", font=("Squares Bold", 24))

    module.create_text(MODULE_WIDTH / 2, 160, text=name, fill="white", font=("Squares Bold", 48))

    data = {"module":module, "orientation":orientation, "temperature":{"module":temperature, "x1":temperature_x1, "y1":temperature_y1, "x2":temperature_x2, "y2":temperature_y2, "text":temperature_text}, "load":{"module":load, "x1":load_x1, "y1":load_y1, "x2":load_x2, "y2":load_y2, "text":load_text, "extent":extent}}

    return data

def update(window, gpu_data):
    gpu_info = subprocess.check_output(["nvidia-smi", "--format=csv", "--query-gpu=utilization.gpu,temperature.gpu,fan.speed"]).decode("utf-8")
    gpu_load, gpu_temperature, gpu_fan_speed = gpu_info.split("\r\n")[1].split(", ")

    gpu_load = int(gpu_load.split()[0])
    gpu_temperature = int(gpu_temperature.split()[0])
    gpu_fan_speed = int(gpu_fan_speed.split()[0])

    if gpu_temperature < 70:
        gpu_temperature_module_color = "green"
        gpu_temperature_text_color = "white"
    elif gpu_temperature < 90:
        gpu_temperature_module_color = "yellow"
        gpu_temperature_text_color = "black"
    else:
        gpu_temperature_module_color = "red"
        gpu_temperature_text_color = "black"

    gpu_data["module"].coords(gpu_data["temperature"]["module"], gpu_data["temperature"]["x1"], gpu_data["temperature"]["y1"], int(WIDTH * gpu_temperature / 100), gpu_data["temperature"]["y2"])
    gpu_data["module"].itemconfigure(gpu_data["temperature"]["module"], fill=gpu_temperature_module_color)

    gpu_data["module"].itemconfigure(gpu_data["temperature"]["text"], fill=gpu_temperature_text_color, text=f"{gpu_temperature}°C")

    if gpu_load < 70:
        gpu_load_module_color = "green"
        gpu_load_text_color = "white"
    elif gpu_load < 90:
        gpu_load_module_color = "yellow"
        gpu_load_text_color = "black"
    else:
        gpu_load_module_color = "red"
        gpu_load_text_color = "black"
    
    if gpu_data["orientation"]:
        gpu_data["module"].itemconfigure(gpu_data["load"]["module"], fill=gpu_load_module_color, extent=int(-180 * gpu_load / 100))
    else:
        gpu_data["module"].itemconfigure(gpu_data["load"]["module"], fill=gpu_load_module_color, extent=int(180 * gpu_load / 100))

    gpu_data["module"].itemconfigure(gpu_data["load"]["text"], fill=gpu_load_text_color, text=f"{gpu_load}%")

    window.after(256, update, window, gpu_data)

if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("systeminfo")
    window.geometry("480x384")
    window.configure(background="black", border=0)

    author = tkinter.Canvas(window, width=400, height=48, background="black", highlightthickness=0)
    author.pack()
    author.place(x=8, y=328)

    author.create_text(48, 24, text="BY", fill="white", font=("Squares Bold", 48))
    author.create_text(180, 12, text="dekxrma", fill="white", font=("Squares Bold", 20))
    author.create_text(240, 36, text="ArtikTheOnlyOne", fill="white", font=("Squares Bold", 20))

    update(window, module(window, "GPU", False, 0, 0))

    window.mainloop()