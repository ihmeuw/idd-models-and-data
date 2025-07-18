rm(list = ls())
require(RColorBrewer)

true_beta = 2
true_gamma = 1
true_rho = 0.25
true_i0 = 0.01
true_rho = 0.25
true_N = 100

guess_beta = 1.8
guess_gamma = 1.1

obs_weeks = 2:7

drho <- 0.01
rho_vec <- seq(drho, 1 - drho, by = drho)

complete_pars <- function(beta = guess_beta, gamma = guess_gamma, N = true_N, 
                          i0 = true_i0, rho = true_rho, duration = 20, dt = 1){
  pars = data.frame(beta = beta, gamma = gamma, N = N,
                    i0 = i0, rho = rho, duration = duration, dt = dt)
  return(pars)
}

run_SIR <- function(pars){
  beta = pars[['beta']]
  gamma = pars[['gamma']]
  N = pars[['N']]
  i0 = pars[['i0']]
  rho = pars[['rho']]
  dt = pars[['dt']]
  duration = pars[['duration']]
  dt = pars[['dt']]
  times = seq(0,duration, by = dt)
  SIR_df = data.frame(time = times, 
                      S = 0, I = 0, R = 0, newI = 0, newC = 0)
  SIR_df$I[1] <- round(i0*N)
  SIR_df$S[1] <- N - SIR_df$I[1]
  
  for (t_num in seq_along(head(times, -1))){
    S = SIR_df$S[t_num]
    I = SIR_df$I[t_num]
    R = SIR_df$R[t_num]
    #
    newI = round(S * (1 - exp(-beta * I / N * dt)))
    newR = round(I * (1 - exp(-gamma * dt)))
    newC = rbinom(1, newI, prob = rho)
    #
    SIR_df$S[t_num + 1] = S - newI
    SIR_df$I[t_num + 1] = I + newI - newR
    SIR_df$R[t_num + 1] = R + newR
    SIR_df$newI[t_num] = newI
    SIR_df$newC[t_num] = newC
  }
  return(SIR_df)
}

true_pars = complete_pars(beta = true_beta, gamma = true_gamma)
true_df = run_SIR(true_pars)



SIR_COLS = brewer.pal(4, 'Set1')[c(3, 1, 2, 4)]

LL_COLS = brewer.pal(length(obs_weeks), 'Set2')

obs_df <- true_df[which(true_df$time %in% obs_weeks), c("time", "newC")]

plot_sir = function(df, rho){
  time = df[['time']]
  S = df[['S']]
  I = df[['I']]
  R = df[['R']]
  newI = df[['newI']]
  
  obs_weeks = obs_df[['time']]
  #
  plot(time, S, type = 'l', xlab = 'Time', ylab = 'Population', ylim = c(0, max(S+I+R)), lwd = 2, col = SIR_COLS[1])
  lines(time, I, lwd = 2, col = SIR_COLS[2])
  lines(time, R, lwd = 2, col = SIR_COLS[3])
  #
  obs_locs <- which(time %in% obs_weeks)
  plot(time, newI, col = SIR_COLS[2], pch = 19)
  points(obs_df$time, obs_df$newC, col = SIR_COLS[4], pch = 4, lwd = 2)
  points(time[obs_locs], rho * newI[obs_locs], col = SIR_COLS[2], cex = 2, lwd = 2)
}


plot_single_likelihood_cont <- function(newI, newC, o_num){
  tmp_x <- rho_vec
  tmp_y <- dbinom(newC, newI, prob = rho_vec, log = TRUE)
  YMAX <- max(tmp_y)
  YMIN <- max(tmp_y) - 10
  YLIM = c(YMIN, YMAX)
  plot(tmp_x, tmp_y, ylim = YLIM, col = LL_COLS[o_num], type = 'l', lwd = 2)
}

get_ll_df <- function(df, obs_df){
  obs_weeks = obs_df[['time']]
  df = df[which(df[['time']] %in% obs_weeks),]
  
  ll_df <- sapply(rho_vec, function(x){
    dbinom(obs_df[['newC']], df[['newI']], prob = x, log = TRUE)
  })
 
  return(ll_df)
}

# ll_df <- get_ll_df(df, obs_df)

plot_total_likelihood_cont <- function(df, obs_df, logl = TRUE){
  obs_weeks = obs_df[['time']]
  df = df[which(df[['time']] %in% obs_weeks),]
  
  tmp_x <- rho_vec
  
  
  if (logl){
    tmp_y <- sapply(rho_vec, function(x){
      sum(dbinom(obs_df[['newC']], df[['newI']], prob = x, log = TRUE))
    })
    YMAX <- max(tmp_y)
    YMIN <- max(tmp_y) - 10
  } else {
    tmp_y <- sapply(rho_vec, function(x){
      prod(dbinom(obs_df[['newC']], df[['newI']], prob = x, log = FALSE))
    })
    YMAX <- max(tmp_y)
    YMIN <- 0
  }
  
  
  plot(tmp_x, tmp_y, ylim = c(YMIN,YMAX), lwd = 2, col = 1, type = 'l')
  mle <- rho_vec[which.max(tmp_y)]
  abline(v = mle, lty = 2)
  abline(h = max(tmp_y), lty = 2)
}

plot_obs <- function(rho, df, obs_df){
  obs_weeks = obs_df[['time']]
  for (o_num in seq_along(obs_weeks)){
    tmp_newI <- df$newI[which(df$time == obs_weeks[o_num])]
    tmp_newC <- obs_df$newC[which(obs_df$time == obs_weeks[o_num])]
    plot_single_likelihood_cont(newI = tmp_newI, newC = tmp_newC, o_num = o_num)
  }
}

make_plot <- function(pars, obs_df){
  panels = c(1, 3, 4, 5, 1, 3, 4, 5,
             1, 6, 7, 8, 2, 6, 7, 8,
             2, 9, 9, 9, 2, 9, 9, 9)
  
  df = run_SIR(pars)
  rho = pars[['rho']]

  layout(matrix(panels, 6, 4, byrow = TRUE),
         widths = c(3,1,1,1)) 
  par(mar=c(5.1,5.1,1.1,2.1), oma = c(0,0,3,2))
  plot_sir(df, rho)
  par(mar=c(2.1,2.1,1.1,.1))  
  plot_obs(rho, df, obs_df)
  #
  par(mar = c(5.1,2.1,2.1,.1))
  plot_total_likelihood_cont(df, obs_df, logl = TRUE)
}




# Start with rho from previous page
pars = complete_pars(beta = guess_beta, gamma = guess_gamma)
df = run_SIR(pars)
pars[['rho']] = get_mle(df, obs_df)

make_plot(pars, obs_df)



ll_df <- get_ll_df(df, obs_df)
YMAX = max(ll_df[1,])
YMIN = max(colSums(ll_df)) - 20
YLIM = c(YMIN, YMAX)
require(glue)
par(mfrow = c(2,3))
for (o_num in 1:6){
  lower = upper <- ll_df[1,]
  plot(rho_vec, upper, col = LL_COLS[1], lwd = 2, type = 'l', ylim = YLIM)
  if (o_num > 1){
    for (o_two in 2:o_num){
      tmp_col = adjustcolor(LL_COLS[o_two], alpha = 0.4)
      lower = upper + ll_df[o_two,]
      polygon(c(rho_vec, rev(rho_vec)), c(lower, rev(upper)), col = tmp_col, border = NA)
      lines(rho_vec, lower, lwd = 2, col = LL_COLS[o_two])
      upper = lower
    }
  }
  tmp_max = max(lower)
  tmp_max_loc = which.max(lower)
  tmp_mle = rho_vec[tmp_max_loc]
  lines(rep(tmp_mle, 2), c(tmp_max - 2, tmp_max), lwd = 2)
  tmp_in_CI = which(lower > tmp_max - 2)
  tmp_lci_loc = min(tmp_in_CI)
  tmp_lci = rho_vec[tmp_lci_loc]
  tmp_uci_loc = max(tmp_in_CI)
  tmp_uci = rho_vec[tmp_uci_loc]
  lines(c(tmp_lci, tmp_uci), rep(tmp_max - 2, 2), lwd = 2)
  tmp_txt = glue("mle: {100*tmp_mle}%")
  tmp_txt_2 = glue('95% CI: {100*tmp_lci}% - {100*tmp_uci}%')
  text(tmp_mle, tmp_max-3, tmp_txt)
  text(tmp_mle, tmp_max-5, tmp_txt_2)
}
