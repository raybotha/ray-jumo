import random
import faker
import time
import sys

start = time.perf_counter()
fake = faker.Faker()

zeros = int(sys.argv[1])
total_loans = 10**zeros
f = open('generated_loans.csv', 'w')
print("MSISDN,Network,Date,Product,Amount", file=f)
progress = 0
for i in range(total_loans):
    line = ["27812320741",
            "'Network {}'".format(random.randint(1,3)),
            fake.date_time_between(start_date="-1y").strftime("'%d-%b-%Y'"),
            "'Loan Product {}'".format(random.randint(1,3)),
            "{:0.2f}".format(random.uniform(1,10000))]
    line_string = ",".join(line)
    print(line_string, file=f)
    if i % 10000 == 0:
        print(str("{:0.1f}% of task done".format((i / total_loans) * 100)))

end = time.perf_counter()
elapsed = end - start
print("Done. Task duration = {:.12f} seconds for {} million rows".format(elapsed,total_loans/1000000))