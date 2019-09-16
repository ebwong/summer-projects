# Command-line prompting for users to interact with the data set.
# Not currently used
def prompt_user():
    welcome_msg = "Welcome to a tool for investigating data from the 2014 " \
                  "ASE. Choose two different variables from the list below(" \
                  "Type the code in all-caps):"

    print(welcome_msg)

    var_options_msg = "Number of employees: EMP\n" \
                      "Annual payroll: PAYANN\n" "" \
                      "Payroll per employee: PAYPEREMP\n" \
                      "Years in business: YIBSZFI\n"

    var_options = ["EMP", "PAYANN", "PAYPEREMP", "YIBSZFI"]
    print(var_options_msg)

    xvar = None
    yvar = None
    xvar_prompt = "Choose 1 variable to plot on the x-axis:"
    yvar_prompt = "Choose 1 variable to plot on the y-axis"
    var_err_msg_str = " is not a valid variable."

    while True:
        print(xvar_prompt)
        xvar = input()
        if xvar not in var_options:
            print(f"{xvar}" + var_err_msg_str)
            xvar = None
            yvar = None
            continue
        print(yvar_prompt)
        yvar = input()
        if yvar not in var_options:
            print(f"{yvar}" + var_err_msg_str)
            xvar = None
            yvar = None
            continue
        break

    return xvar, yvar