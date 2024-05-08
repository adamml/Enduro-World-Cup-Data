import polars
import matplotlib.pyplot as plt

df = polars.read_json("data/data.json")

df = df.filter(
        polars.col('event_year') == 2023,
        polars.col('event_year_sequence') == 7,
        polars.col('elite_m_or_f') == 'F'
    )

riders = []
event_time_delta = []
event_time_percentage = []
x = []
stage_pos = []
stage_time = []

i = 0
while i < len(df):
    riders.append(df.row(i)[5])
    event_time_delta.append(df.row(i)[13])
    try:
        event_time_percentage.append(((df.row(i)[12]/df.row(0)[12])-1)*100)
    except TypeError:
        event_time_percentage.append(None)
    stage_pos.append([x['position'] for x in df.row(i)[15]])
    stage_time.append([x['stage_time_seconds'] for x in df.row(i)[15]])
    x.append(i+1)
    i += 1

f, a = plt.subplots(1, 2, layout='constrained')
f.suptitle("Finish Spread")
a[0].scatter(event_time_delta, x)
a[0].set_xlabel("Time delta (seconds)")
a[0].set_ylabel("Finish position")

for i, z in enumerate(x):
    if event_time_delta[i] is not None:
        try:
            a[0].annotate(riders[i], (event_time_delta[i], z), fontsize=8)
        except TypeError:
            pass

a[1].plot(x, event_time_percentage)
a[1].set_ylabel("Time delta (%)")
a[1].set_xlabel("Finish position")

a[0].set_ylim(a[0].get_ylim()[::-1])
a[1].set_ylim(a[1].get_ylim()[::-1])
plt.show()

stage_pos_2 = zip(*stage_pos)
stage_time_2 = zip(*stage_time)
