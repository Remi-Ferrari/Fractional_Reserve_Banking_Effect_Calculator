from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    total_value = []
    end_number = []
    multiplicative_change = []
    Sum_Total = []
    Value_Change = []
    Multiplicative_Value_Change = []
    ranks = []

    if request.method == "POST":
        init_dep = float(request.form["initial_deposit"])
        fractional_reserve_val = float(request.form["fractional_reserve"])

        if fractional_reserve_val < 0 or fractional_reserve_val > 100:
            error = "Fractional Reserve value % must be between 0 and 100."
            return render_template("index.html", error=error)
 
        elif fractional_reserve_val == 0:
            return render_template("index.html", result="Infinite money loop has been created.")

        # Calculate banking effect
        result, total_value, end_number, multiplicative_change, Sum_Total, Value_Change, Multiplicative_Value_Change, = calculate_banking_effect(
            init_dep, fractional_reserve_val)

        ranks = list(range(1, end_number + 1)) if end_number > 0 else []
        '''
        #debugging
                print(f"Chart Data: {Sum_Total}")
                print(f"Ranks: {ranks}")

                if not isinstance(Sum_Total, list) or not isinstance(ranks, list):
                    print("Sum_Total or ranks are not lists")
                else:
                    print("Sum_Total and ranks are lists")

                print("Chart Data:", json.dumps(Sum_Total))  # Should print a valid JSON array
                print("Ranks:", json.dumps(ranks))  # Should print a valid JSON array
        #end debug
        '''
        return render_template("index.html",
                               result=result,
                               total_value=total_value,
                               end_number=end_number,
                               multiplicative_change=multiplicative_change,
                               Sum_Total=Sum_Total,
                               Value_Change=Value_Change,
                               Multiplicative_Value_Change=Multiplicative_Value_Change,
                               ranks=ranks)

    return render_template("index.html", Value_Change=json.dumps(Value_Change), Sum_Total=json.dumps(Sum_Total),
                           Multiplicative_Value_Change=json.dumps(Multiplicative_Value_Change), ranks=json.dumps(ranks))


# Function to calculate effect
def calculate_banking_effect(init_dep, fractional_reserve_val):
    output = []
    u = init_dep
    prev_u = u
    rank = 0
    sum_total = u
    Sum_Total = []
    Value_Change = []
    Multiplicative_Value_Change = []

    while u > 0.01:
        prev_u = u
        u *= ((100 - fractional_reserve_val) / 100)
        rank += 1
        sum_total += u  # Accumulate total value
        mvc = u / prev_u  # Multiplicative value change relative to previous value (constant)
        mltpv = sum_total / init_dep  # Multiplicative value relative to starting value

        # Collect chart data
        Sum_Total.append(round(sum_total, 2))
        Value_Change.append(round(u, 2))
        Multiplicative_Value_Change.append(round(mvc, 4))

        # Append to output list
        output.insert(0,
                      f"#{rank}︱ Value: {round(u, 2)}︱ MVC: {round(mvc, 4)}︱ Total: {round(sum_total, 2)}︱ Multiplicative value: {round(mltpv, 4)}")

    # Values for summary statistics
    total_value = round(sum_total, 2)
    end_number = rank
    multiplicative_change = mltpv

    return output, total_value, end_number, round(multiplicative_change,
                                                  4), Sum_Total, Value_Change, Multiplicative_Value_Change


if __name__ == "__main__":
    app.run(debug=True)

