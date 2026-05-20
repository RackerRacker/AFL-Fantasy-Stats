library(fitzRoy)
library(dplyr)

fixture <- fetch_fixture(2025, comp = "AFLM")

# Save the selected data to a new variable
clean_fixture <- fixture %>%
  select(
    round.name,
    home.team.name, away.team.name, venue.name
  )

# Write to CSV
write.csv(clean_fixture, "~/Desktop/AFL Fixture/afl_fixture_2025.csv", row.names = FALSE)