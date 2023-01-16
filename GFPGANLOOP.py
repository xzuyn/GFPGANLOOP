import os
import shutil
import time

PROCESSED_IMAGES = []
FINAL_IMAGES = []
MODEL = "1.4"
MODELinput = ""
ACCEPTED_MODELS = ["1", "1.2", "1.3", "1.4"]
FIRSTSCALEFACTOR = "2"
FSFinput = ""


def isFloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


MODELinput = input(f"Model (1, 1.2, 1.3, or 1.4) [Default: {MODEL}]: ")
FSFinput = input(f"First scaling factor [Default: {FIRSTSCALEFACTOR}]: ")


# Step 0. If statements.
tic = time.perf_counter()
print()
if MODELinput == "":
    print(f"Using default model: {MODEL}")

if MODELinput != "":
    if MODELinput in ACCEPTED_MODELS:
        MODEL = MODELinput
        print(f"Using model: {MODEL}")
        MODELinput = ""

    else:
        print(f"Invalid model. Using default model: {MODEL}")
        MODELinput = ""

if FSFinput == "":
    print(f"Using default first scaling factor: {FIRSTSCALEFACTOR}")

if FSFinput != "":
    if FSFinput.isdigit():
        FIRSTSCALEFACTOR = str(FSFinput)
        print(f"Using first scaling factor: {FIRSTSCALEFACTOR}")
        FSFinput = ""

    elif isFloat(FSFinput) == True:
        print(
            f"Invalid scaling factor. Cannot be a float value. Converting to integer."
        )
        print(f"Converted Float: {float(FSFinput)} to {int(float(FSFinput))}")

        FIRSTSCALEFACTOR = str(int(float(FSFinput)))
        print(f"Using first scaling factor: {FIRSTSCALEFACTOR}")
        FSFinput = ""

    else:
        print(
            f"Invalid scaling factor. Using default first scaling factor: {FIRSTSCALEFACTOR}"
        )
        FSFinput = ""

# Step 1. 2x GFPGAN.
ticSTEP1 = time.perf_counter()
print()
print()
print(f"Step 1: {FIRSTSCALEFACTOR}x GFPGAN using {MODEL} model.")
os.system(
    f"python inference_gfpgan.py -i LOOPINPUT -o LOOPTEMP\\LOOPRESULT_{FIRSTSCALEFACTOR}x_{MODEL} -v {MODEL} -s {FIRSTSCALEFACTOR}"
)
tocSTEP1 = time.perf_counter()

# Step 2. 2-1x GFPGAN.
ticSTEP2 = time.perf_counter()
print()
print()
print(f"Step 2: {FIRSTSCALEFACTOR}-1x GFPGAN using {MODEL} model.")
os.system(
    f"python inference_gfpgan.py -i LOOPTEMP\\LOOPRESULT_{FIRSTSCALEFACTOR}x_{MODEL}\\restored_imgs -o LOOPTEMP\\LOOPRESULT_{FIRSTSCALEFACTOR}-1x_{MODEL} -v {MODEL} -s 1"
)
tocSTEP2 = time.perf_counter()

# Step 3. 2-1-1x GFPGAN.
ticSTEP3 = time.perf_counter()
print()
print()
print(f"Step 3: {FIRSTSCALEFACTOR}-1-1x GFPGAN using {MODEL} model.")
os.system(
    f"python inference_gfpgan.py -i LOOPTEMP\\LOOPRESULT_{FIRSTSCALEFACTOR}-1x_{MODEL}\\restored_imgs -o LOOPTEMP\\LOOPRESULT_{FIRSTSCALEFACTOR}-1-1x_{MODEL} -v {MODEL} -s 1"
)
tocSTEP3 = time.perf_counter()

if not os.path.exists("LOOPRESULT"):
    os.makedirs("LOOPRESULT")

for RESULTIMAGE in os.listdir(
    f"LOOPTEMP\LOOPRESULT_{FIRSTSCALEFACTOR}-1-1x_{MODEL}\\restored_imgs"
):
    current_name, current_extension = os.path.splitext(RESULTIMAGE)
    shutil.move(
        f".\LOOPTEMP\LOOPRESULT_{FIRSTSCALEFACTOR}-1-1x_{MODEL}\\restored_imgs\\{current_name}{current_extension}",
        f".\LOOPRESULT\\{current_name}_{FIRSTSCALEFACTOR}-1-1x_{MODEL}{current_extension}",
    )
    PROCESSED_IMAGES.append(str(current_name) + str(current_extension))
    FINAL_IMAGES.append(
        str(current_name)
        + (f"_{FIRSTSCALEFACTOR}-1-1x_{MODEL}")
        + str(current_extension)
    )

shutil.rmtree(".\LOOPTEMP")

print("------")
print()
print()
print("Processed Images: ")

for P_IMGS in PROCESSED_IMAGES:
    print(f"LOOPINPUT\\{P_IMGS}")

print()
print("Final Images: ")
for F_IMGS in FINAL_IMAGES:
    print(f"LOOPRESULT\\{F_IMGS}")

print()
print(
    f"Step 1: {FIRSTSCALEFACTOR}x completed in {tocSTEP1 - ticSTEP1:0.4f} seconds."
)
print(
    f"Step 2: {FIRSTSCALEFACTOR}-1x completed in {tocSTEP2 - ticSTEP2:0.4f} seconds."
)
print(
    f"Step 3: {FIRSTSCALEFACTOR}-1-1x completed in {tocSTEP3 - ticSTEP3:0.4f} seconds."
)

toc = time.perf_counter()
print(f"Entire process completed in {toc - tic:0.4f} seconds.")
