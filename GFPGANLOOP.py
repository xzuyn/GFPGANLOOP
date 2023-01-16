import os
import shutil
import time

PROCESSED_IMAGES = []
FINAL_IMAGES = []
MODEL = "1.4"
ACCEPTED_MODELS = ["1", "1.2", "1.3", "1.4"]
FIRSTRUNSCALE = "2"
MODELinput = ""


MODELinput = input("Model (1, 1.2, 1.3, or 1.4) [Default: " + MODEL + "]: ")

tic = time.perf_counter()

if MODELinput == "":
    print("Using default model: " + MODEL)


if MODELinput != "":
    if MODELinput in ACCEPTED_MODELS:
        MODEL = MODELinput
        print("Using model: " + MODEL)

    else:
        print("Invalid model. Using default model: " + MODEL)
        MODELinput = ""

# Step 1. 2x GFPGAN.
ticSTEP1 = time.perf_counter()
print()
print()
print("Step 1: " + FIRSTRUNSCALE + "x GFPGAN using " + MODEL + " model.")
os.system(
    "python inference_gfpgan.py -i LOOPINPUT -o LOOPTEMP\\LOOPRESULT-2x_"
    + MODEL
    + " -v "
    + MODEL
    + " -s "
    + FIRSTRUNSCALE
)
tocSTEP1 = time.perf_counter()

# Step 2. 2x-1x GFPGAN.
ticSTEP2 = time.perf_counter()
print()
print()
print("Step 2: " + FIRSTRUNSCALE + "x-1x GFPGAN using " + MODEL + " model.")
os.system(
    "python inference_gfpgan.py -i LOOPTEMP\\LOOPRESULT-2x_"
    + MODEL
    + "\\restored_imgs -o LOOPTEMP\\LOOPRESULT-2x-1x_"
    + MODEL
    + " -v "
    + MODEL
    + " -s 1"
)
tocSTEP2 = time.perf_counter()

# Step 3. 2x-1x-1x GFPGAN.
ticSTEP3 = time.perf_counter()
print()
print()
print("Step 3: " + FIRSTRUNSCALE + "x-1x-1x GFPGAN using " + MODEL + " model.")
os.system(
    "python inference_gfpgan.py -i LOOPTEMP\\LOOPRESULT-2x-1x_"
    + MODEL
    + "\\restored_imgs -o LOOPTEMP\\LOOPRESULT-2x-1x-1x_"
    + MODEL
    + " -v "
    + MODEL
    + " -s 1"
)
tocSTEP3 = time.perf_counter()


if not os.path.exists("LOOPRESULT"):
    os.makedirs("LOOPRESULT")


for RESULTIMAGE in os.listdir(
    "LOOPTEMP\LOOPRESULT-2x-1x-1x_" + MODEL + "\\restored_imgs"
):
    current_name, current_extension = os.path.splitext(RESULTIMAGE)
    shutil.move(
        ".\LOOPTEMP\LOOPRESULT-2x-1x-1x_"
        + MODEL
        + "\\restored_imgs\\"
        + current_name
        + current_extension,
        ".\LOOPRESULT\\"
        + current_name
        + "-2x-1x-1x_"
        + MODEL
        + current_extension,
    )
    PROCESSED_IMAGES.append(str(current_name) + str(current_extension))
    FINAL_IMAGES.append(
        str(current_name) + "-2x-1x-1x_" + MODEL + str(current_extension)
    )

shutil.rmtree(".\LOOPTEMP")

print("------")
print()
print()
print("Processed Images: ")

for P_IMGS in PROCESSED_IMAGES:
    print("LOOPINPUT\\" + P_IMGS)

print()
print("Final Images: ")
for F_IMGS in FINAL_IMAGES:
    print("LOOPRESULT\\" + F_IMGS)


toc = time.perf_counter()

print()
print(f"Step 1: 2x completed in {tocSTEP1 - ticSTEP1:0.4f} seconds.")
print(f"Step 2: 2x-1x completed in {tocSTEP2 - ticSTEP2:0.4f} seconds.")
print(f"Step 3: 2x-1x-1x completed in {tocSTEP3 - ticSTEP3:0.4f} seconds.")
print(f"Entire process completed in {toc - tic:0.4f} seconds.")
