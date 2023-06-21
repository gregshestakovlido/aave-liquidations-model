import numpy as np
import pandas as pd
import streamlit as st
DUNE_KEY = st.secrets['dune_key']
TOKEN = st.secrets['infura']  #Infura, blastapi, etc..

# v2 contracts

AAVE2_LPOOL_CONTRACT = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9" #Aave v2 Lending Pool Contract
AAVE2_ORACLE_CONTRACT = "0xA50ba011c48153De246E5192C8f9258A2ba79Ca9" # Aave Oracle Contract
ASTETH_CONTRACT = "0x1982b2F5814301d4e9a8b0201555376e62F82428" #aSTETH token

AAVE2_LTV = 0.72 #0.69 #LTV for stETH reserve
AAVE2_LIQUIDATION_THRESHOLD = 0.83 #0.81 # liq. threshold for stETH reserve
AAVE2_CLOSE_FACTOR = 0.5 
AAVE2_LIQUIDATION_BONUS = 1.07 # 1.075
STETH_START_AMOUNT_CASCADE_LIQUDATIONS = 80000 #start_amount - amount of stETH from which estimation of possible cascade liq begins >= 20k
STEP_CASCADE_LIQUDATIONS = 1000 #step with wich estimation of possible cascade liq is doing

risk_rating = ['A','B+','B','B-','C','D','liquidation']
b1v2_collateral_loan_ratio = np.array([1.42, 1.21, 1.14, 1.07, 1.03, 1])
b2v2_collateral_loan_ratio = np.array([2.5, 1.75, 1.5, 1.25, 1.1, 1])
b3v2_collateral_loan_ratio = np.array([2.5, 1.75, 1.5, 1.25, 1.1, 1])
#list of collateral stats: token contract, variable debt, stable debt, decimals, penalty, liq.treshold, atoken(collateral)

USDT = ('usdt',"0xdAC17F958D2ee523a2206206994597C13D831ec7", "0x531842cebbdd378f8ee36d171d6cc9c4fcf475ec", "0xe91D55AB2240594855aBd11b3faAE801Fd4c4687", 6, 0, 0,"0x3Ed3B47Dd13EC9a98b44e6204A523E766B225811")
USDC = ('usdc',"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "0x619beb58998ed2278e08620f97007e1116d5d25b", "0xe4922afab0bbadd8ab2a88e0c79d884ad337fca6",6, 0.045, 0.875, "0xBcca60bB61934080951369a648Fb03DF4F96263C")
STETH = ('steth',"0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84", "0xA9DEAc9f00Dc4310c35603FCD9D34d1A750f81Db", "0x66457616Dd8489dF5D0AFD8678F4A260088aAF55",18, 0.07, 0.83,"0x1982b2F5814301d4e9a8b0201555376e62F82428") 
TUSD = ('tusd', "0x0000000000085d4780B73119b644AE5ecd22b376", "0x01C0eb1f8c6F1C1bF74ae028697ce7AA2a8b0E92", "0x7f38d60D94652072b2C44a18c0e14A481EC3C0dd", 18, 0.05, 0.825, "0x101cc05f4A51C0319f570d5E146a8C625198e636")
DAI = ('dai',"0x6B175474E89094C44Da98b954EedeAC495271d0F", "0x6c3c78838c761c6ac7be9f59fe808ea2a6e4379d","0x778a13d3eeb110a4f7bb6529f99c000119a08e92",  18, 0.04, 0.87, "0x028171bCA77440897B824Ca71D1c56caC55b68A3")
SUSD = ('susd',"0x57ab1ec28d129707052df4df418d58a2d46d5f51", "0xdc6a3ab17299d9c2a412b0e0a4c1f55446ae0817","0x30B0f7324feDF89d8eff397275F8983397eFe4af",  18, 0, 0, "0x6C5024Cd4F8A59110119C56f8933403A539555EB")
FEI = ('fei',"0x956F47F50A910163D8BF957Cf5846D573E7f87CA", "0xC2e10006AccAb7B45D9184FcF5b7EC7763f5BaAe","0xd89cF9E8A858F8B4b31Faf793505e112d6c17449", 18, 0, 0.075, "0x683923dB55Fead99A79Fa01A27EeC3cB19679cC3")
WETH = ('weth',"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xF63B34710400CAd3e044cFfDcAb00a0f32E33eCf", "0x4e977830ba4bd783C0BB7F15d3e243f73FF57121",18, 0.05, 0.86, "0x030bA81f1c18d280636F32af80b9AAd02Cf0854e")
WBTC = ('wbtc',"0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", "0x9c39809Dec7F95F5e0713634a4D0701329B3b4d2", "0x51B039b9AFE64B78758f8Ef091211b5387eA717c",8, 0.05, 0.82, "0x9ff58f4fFB29fA2266Ab25e75e2A8b3503311656")
USDP = ('usdp',"0x8E870D67F660D95d5be530380D0eC0bd388289E1", "0xFDb93B3b10936cf81FA59A02A7523B6e2149b2B7", '-',18, 0, 0, "0x2e8F4bdbE3d47d7d7DE490437AeA9915D930F1A3")
FRAX = ('frax',"0x853d955aCEf822Db058eb8505911ED77F175b99e", "0xfE8F19B17fFeF0fDbfe2671F248903055AFAA8Ca", "0x3916e3B6c84b161df1b2733dFfc9569a1dA710c2",18, 0, 0, "0xd4937682df3C8aEF4FE912A96A74121C0829E664")
GUSD = ('gusd',"0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd", "0x279AF5b99540c1A3A7E3CDd326e19659401eF99e", "0xf8aC64ec6Ff8E0028b37EB89772d21865321bCe0",2, 0, 0, "0xD37EE7e4f452C6638c96536e68090De8cBcdb583")
BUSD = ('busd',"0x4Fabb145d64652a948d72533023f6E7A623C7C53", "0xbA429f7011c9fa04cDd46a2Da24dc0FF0aC6099c", "0x4A7A63909A72D268b1D8a93a9395d098688e0e5C",18, 0, 0, "0xA361718326c15715591c299427c62086F69923D9")

#more attractive collaterals (by liqudation bonus)
XSUSHI = ('xsushi',"0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272", "0xfAFEDF95E21184E3d880bd56D4806c4b8d31c69A", "-",18, 0.085, 0.65, "0xF256CC7847E919FAc9B808cC216cAc87CCF2f47a")
CRV = ('crv',"0xD533a949740bb3306d119CC777fa900bA034cd52", "0x00ad8eBF64F141f1C81e9f8f792d3d1631c6c684", "0x9288059a74f589C919c7Cf1Db433251CdFEB874B",18, 0.08, 0.58, "0x8dAE6Cb04688C62d939ed9B68d32Bc62e49970b1")


debt_tokens_v2 = tuple(zip( USDC, USDT, DAI, FEI, TUSD, SUSD, USDP, FRAX, GUSD, BUSD)) #,WETH #WBTC,

more_cuddly_collateral_tokens = tuple(zip( XSUSHI, CRV)) #

#_____________________________
# v3 contracts
WSTETH_CONTRACT = "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0"
AAVE3_LPOOL_CONTRACT = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2" #Aave v3 Lending Pool Contract
AAVE3_ORACLE_CONTRACT = "0x54586bE62E3c3580375aE3723C145253060Ca0C2" # Aave Oracle v3
AWSTETH_CONTRACT = "0x0B925eD163218f6662a35e0f0371Ac234f9E9371" #Aave Ethereum wstETH (aEthwstETH) v3

AAVE3_LTV = 0.685 #0.69 #LTV for stETH reserve
AAVE3_LIQUIDATION_THRESHOLD = 0.795 #0.81 # liq. threshold for stETH reserve

AAVE3_LTV_EMODE = 0.90  #LTV for wstETH reserve e'mode
AAVE3_LIQUIDATION_THRESHOLD_EMODE = 0.93  # liq. threshold for stETH reserve e'mode

AAVE3_CLOSE_FACTOR = 1
AAVE3_LIQUIDATION_BONUS = 1.07 
AAVE3_LIQUIDATION_BONUS_EMODE = 1.01 

b1v3_collateral_loan_ratio = np.array([1.42, 1.21, 1.14, 1.05, 1.03, 1])
b2v3_collateral_loan_ratio = np.array([2.5, 1.75, 1.5, 1.25, 1.1, 1])
b3v3_collateral_loan_ratio = np.array([2.5, 1.75, 1.5, 1.25, 1.1, 1])


#list of collateral stats: token contract, variable debt, stable debt, decimals, penalty, liq.treshold, atoken(collateral), liq treshold e-mode, penalty e-mode
DAI3 = ('dai',"0x6B175474E89094C44Da98b954EedeAC495271d0F", "0xcF8d0c70c850859266f5C338b38F9D663181C314","0x413AdaC9E2Ef8683ADf5DDAEce8f19613d60D1bb",  18, 0.04, 0.77, "0x018008bfb33d285247A21d44E50697654f754e63",0,0)
USDC3 = ('usdc',"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "0x72E95b8931767C79bA4EeE721354d6E99a61D004", "0xB0fe3D292f4bd50De902Ba5bDF120Ad66E9d7a39",6, 0.045, 0.76, "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c",0,0)
USDT3 = ('usdt',"0xdAC17F958D2ee523a2206206994597C13D831ec7", "0x6df1C1E379bC5a00a7b4C6e67A203333772f45A8", "-", 6, 0, 0,"0x23878914EFE38d27C4D67Ab83ed1b93A74D4086a",0,0)
LUSD3 = ('lusd',"0x5f98805A4E8be255a32880FDeC7F6728C6568bA0", "0x33652e48e4B74D18520f11BfE58Edd2ED2cEc5A2", "-", 18, 0, 0,"0x3Fe6a295459FAe07DF8A0ceCC36F37160FE86AA9",0,0)
CBETH3 = ('cbeth',"0xBe9895146f7AF43049ca1c1AE358B0541Ea49704", "0x0c91bcA95b5FE69164cE583A2ec9429A569798Ed", "-",18, 0.075, 0.74,"0x977b6fc5dE62598B08C85AC8Cf2b745874E8b78c", 0.93, 0.01) 
WETH3 = ('weth',"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xeA51d7853EEFb32b6ee06b1C12E6dcCA88Be0fFE", "0x102633152313C81cD80419b6EcF66d14Ad68949A",18, 0.05, 0.825, "0x4d5F47FA6A74757f35C14fD3a6Ef8E3C9BC514E8", 0.93, 0.01)
WSTETH3 = ('wsteth',"0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0", "0xC96113eED8cAB59cD8A66813bCB0cEb29F06D2e4", "0x39739943199c0fBFe9E5f1B5B160cd73a64CB85D",18, 0.07, 0.795,"0x0B925eD163218f6662a35e0f0371Ac234f9E9371", 0.93, 0.01) 
WBTC3 = ('wbtc',"0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", "0x40aAbEf1aa8f0eEc637E0E7d92fbfFB2F26A8b7B", "0x39739943199c0fBFe9E5f1B5B160cd73a64CB85D",8, 0.0625, 0.75, "0x5Ee5bf7ae06D1Be5997A1A72006FE6C607eC6DE8",0,0)
RETH3 = ('reth',"0xae78736Cd615f374D3085123A210448E74Fc6393", "0xae8593DD575FE29A9745056aA91C4b746eee62C8", "-",18, 0.075, 0.74,"0xCc9EE9483f662091a1de4795249E24aC0aC2630f", 0.93, 0.01) 


debt_tokens_v3 = tuple(zip( USDC3, USDT3, DAI3, LUSD3)) #,WETH #WBTC,

